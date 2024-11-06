import argparse
import json
import os
import re
import sys
import pandas as pd


def save_to_csv(list_of_dataframes):
    for df in list_of_dataframes:
        if not os.path.exists("./sceneries"):
            os.makedirs("./sceneries")
        df["data"].to_csv(f"./sceneries/{df['name']}.csv")


def event_mapping(event, t: int, params: dict):
    mapping = params["mapping"]
    mapped = mapping[(mapping.component == event[0]) & (mapping.action == event[1]) & (mapping.target == event[2])]
    e = mapped["class"].iloc[0]
    result = {"event": e, "time": t}
    if params["multilevel"]:
        tf = params["initial_date"] + (params["final_date"] - params["initial_date"]) / 2
        e = e + "_START" if t <= tf else e + "_END"
        result = {"event": e, "time": t}

    return result


def temporal_folding(events, session_gap=3600):
    sessions = []
    current_session = [events[0]]

    for i in range(1, len(events)):
        if events[i]["time"] - events[i - 1]["time"] <= session_gap:
            current_session.append(events[i])
        else:
            sessions.append(current_session)
            current_session = [events[i]]

    sessions.append(current_session)
    return sessions


def coalescing_hidden(events, multilevel=False):
    remove_indexes = []
    suffix = "_START" if multilevel else ""
    end_suffix = "_END" if multilevel else ""

    for i in range(len(events) - 1):
        try:
            if events[i]["event"] == f"assignment_vis{suffix}" and events[i + 1]["event"] in [
                f"assignment_try{suffix}",
                f"assignment_sub{suffix}",
            ]:
                remove_indexes.append(i)
            elif (
                events[i]["event"] == f"assignment_try{suffix}" and events[i + 1]["event"] == f"assignment_sub{suffix}"
            ):
                remove_indexes.append(i)
            elif (
                multilevel
                and events[i]["event"] == f"assignment_vis{end_suffix}"
                and events[i + 1]["event"] in [f"assignment_try{end_suffix}", f"assignment_sub{end_suffix}"]
            ):
                remove_indexes.append(i)
            elif (
                multilevel
                and events[i]["event"] == f"assignment_try{end_suffix}"
                and events[i + 1]["event"] == f"assignment_sub{end_suffix}"
            ):
                remove_indexes.append(i)
        except IndexError:
            pass

    # get index list in reverse order
    remove_indexes = sorted(remove_indexes, reverse=True)
    # drop elements in place
    for index in remove_indexes:
        del events[index]


def coalescing_repeating(events):
    remove_indexes = []
    for i in range(len(events)):
        try:
            if events[i]["event"] == events[i + 1]["event"]:
                if re.match(r"^assignment_sub(_START|_END)?$", events[i]["event"]):
                    remove_indexes.append(i)
                else:
                    remove_indexes.append(i + 1)
        except IndexError:
            pass
    # get index list in reverse order
    remove_indexes = sorted(remove_indexes, reverse=True)
    # drop elements in place
    for index in remove_indexes:
        del events[index]


def spell(events):
    remove_indexes = []
    for i in range(len(events)):
        try:
            spell_length = 1
            index = i
            while events[index]["event"] == events[index + 1]["event"]:
                spell_length += 1
                index += 1
            if events[i]["event"] == events[i + 1]["event"]:
                if re.match(r"^assignment_sub(_START|_END)?$", events[i]["event"]):
                    remove_indexes.append(i)
                else:
                    remove_indexes.append(i + 1)
            # events[i]["event"] = events[i]["event"] + f"-{spell_length}"
            if 2 < spell_length <= 5:
                events[i]["event"] = events[i]["event"] + f"_SOME"
            elif spell_length > 5:
                events[i]["event"] = events[i]["event"] + f"_MANY"
        except IndexError:
            pass
    # get index list in reverse order
    remove_indexes = sorted(remove_indexes, reverse=True)
    # drop elements in place
    for index in remove_indexes:
        del events[index]


# return a sequence of catalogued events based on a dataframe of events
def generate_sequence_from_df(df, params: dict):
    e = list(df.apply(lambda x: event_mapping([x.component, x.action, x.target], x.t, params), axis=1))
    e.pop(0)
    flag = False
    events = []
    for event in reversed(e):
        if (re.match(r"^assignment_sub(_START|_END)?$", event["event"])) and not flag:
            flag = True
        if flag:
            events.append(event)
    events = list(reversed(events))

    if not events:
        return None

    if params["tf"]:
        sessions = temporal_folding(events)

    else:
        sessions = [events]

    for session in sessions:
        if params["coalescing_repeating"]:
            coalescing_repeating(session)
        if params["coalescing_hidden"]:
            coalescing_hidden(session, params["multilevel"])
        if params["spell"]:
            spell(session)
    return sessions

    # if params["coalescing_repeating"]:
    #     coalescing_repeating(events)
    #
    # if params["coalescing_hidden"]:
    #     coalescing_hidden(events, params["multilevel"])
    #
    # if params["spell"]:
    #     spell(events)
    #
    # return events


# make the database ready for GSP and prefix datamining algorithms
def prepare_database(df, params: dict, grade_df=None) -> list:
    events_by_user = []
    unique_users = df.drop_duplicates(subset=["userid"])
    unique_users = unique_users["userid"].tolist()

    for userid in unique_users:
        events = generate_sequence_from_df(df[df.userid == userid], params)
        if events:
            new_user = {"key": str(userid), "events": events, "temporal_folding": params["tf"]}
            if grade_df is not None:
                # print(userid)
                user_grade = grade_df.query(f"userid == {userid}")["student_grade"]
                if user_grade.empty:
                    user_grade = 0.0
                else:
                    user_grade = user_grade.iloc[0]
                new_user["grade"] = user_grade
                new_user["max_grade"] = grade_df["max_grade"].iloc[0]
            events_by_user.append(new_user)
    # print(json.dumps(events_by_user[0], indent=2, default=lambda o: str(o)))
    return events_by_user


def partitioning(params, grade_df=None):
    all_logs_data = params["data"]

    init_date = params["initial_date"]
    final_date = params["final_date"]
    assignment_id = params["assignment_id"]
    grades = None
    activity_logs = (
        all_logs_data.sort_values("t")
        .query(f"t >= {init_date} & t <= {final_date}")
        .query(f"assignment_id == {assignment_id} | component != 'core' & component != 'mod_page'")
        # .query(f"t >= 1573527600 & t <= 1574218500")
    )

    first_access = all_logs_data.sort_values("t").drop_duplicates(subset=["userid"])
    first_access = first_access.sort_values("userid")

    if grade_df is not None:
        grades = grade_df.query(f"id == {assignment_id}")
        # .query(f"time_open >= {init_date} & time_close <= {final_date}"))  # ["userid", "student_grade", "max_grade"]

    return [first_access, activity_logs, grades]


def classify_events(activity, first_access):
    return pd.concat([first_access, activity])  # .sort_values("userid")


def get_dates(params: dict) -> dict:
    quiz = params["quiz"]

    t_open = quiz.query(f"id == {params["assignment_id"]}")["t_open"].iloc[0]
    t_close = quiz.query(f"id == {params["assignment_id"]}")["t_close"].iloc[0]

    params["initial_date"] = t_open
    params["final_date"] = t_close

    return params


def read_params(argv=None) -> dict:
    parser = argparse.ArgumentParser(description="Process command-line parameters for temporal folding and file paths.")

    parser.add_argument("-p", "--path", type=str, required=True, help="Path of the log file")
    parser.add_argument("-sp", "--save-path", type=str, required=True, help="Path to save the file")
    parser.add_argument("-pg", "--grade-path", type=str, required=True, help="Path of grades CSV file")
    parser.add_argument("-pq", "--quiz-path", type=str, required=True, help="Path of quiz CSV file")
    parser.add_argument("-mp", "--mapping-path", type=str, required=True, help="Path of event mapping CSV file")
    parser.add_argument("-act", "--activity", type=int, required=True, help="Activity ID")
    parser.add_argument("-id", "--assignment-id", type=int, required=True, help="Assignment ID")
    parser.add_argument("-tf", "--temporal-folding", action="store_true", help="Enable temporal folding")
    parser.add_argument("-m", "--multilevel", action="store_true", help="Enable multilevel sequential patterns")
    parser.add_argument("-r", "--coalescing-repeating", action="store_true", help="Enable coalescing repeating")
    parser.add_argument("-c", "--coalescing-hidden", action="store_true", help="Enable coalescing hidden")
    parser.add_argument(
        "-s", "--spell", action="store_true", help="Enable spell option and disable coalescing repeating"
    )

    # Parse the arguments
    # args = parser.parse_args(argv)
    args = parser.parse_args(argv[1:] if argv else None)

    # Prepare the params dictionary with parsed arguments
    params = {
        "path": args.save_path,
        "grade_path": args.grade_path,
        "quiz_path": args.quiz_path,
        "activity": args.activity,
        "assignment_id": args.assignment_id,
        "tf": args.temporal_folding,
        "coalescing_repeating": args.coalescing_repeating,
        "coalescing_hidden": args.coalescing_hidden,
        "spell": args.spell,
        "multilevel": args.multilevel,
        "data": pd.read_csv(args.path, index_col="id").sort_values("t"),
        "mapping": pd.read_csv(args.mapping_path),
        "quiz": pd.read_csv(args.quiz_path),
    }

    # Override coalescing_repeating if spell option is enabled
    if args.spell:
        params["coalescing_repeating"] = False

    params = get_dates(params)

    return params


def main(params: dict):
    grade_df = pd.read_csv(params["grade_path"])
    first_access, activity, grades = partitioning(params, grade_df)
    activity = classify_events(activity, first_access)

    events_by_user = prepare_database(activity, params, grades)
    os.makedirs(params["path"], exist_ok=True)

    with open(params["path"] + "user.json", "w+") as file:
        json.dump(events_by_user, file, indent=2, default=lambda o: str(o))


if __name__ == "__main__":
    main(read_params(sys.argv))
