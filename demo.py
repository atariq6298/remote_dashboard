from pandas import *


def get_graph_three_data():
    loc = ".\\target_output_new.xls"
    xls = ExcelFile(loc)
    queryset = xls.parse(xls.sheet_names[0], converters={'Release': str})
    releases = get_all_releases(queryset)
    dict_ret = get_test_case_count_isb(queryset, releases)
    return dict_ret


def get_test_case_count_isb(queryset, list_releases):
    data_us_comp_isb = []
    data_us_comp_other = []
    data_bdd_per_story_isb = []
    data_bdd_per_story_other = []
    for release in list_releases:
        queryset_release = queryset[queryset['Release'] == release]
        queryset_release_isb = queryset_release[queryset_release['location'] == "ISL"]
        queryset_release_other = queryset_release[~(queryset_release['location'] == "ISL")]

        total_us_islamabad = queryset_release_isb.sum(axis=0, skipna=True)["US count"]
        total_us_others = queryset_release_other.sum(axis=0, skipna=True)["US count"]

        total_us_points_islamabad = queryset_release_isb.sum(axis=0, skipna=True)["Total Story Points"]
        total_us_points_others = queryset_release_other.sum(axis=0, skipna=True)["Total Story Points"]

        total_bdd_isb = queryset_release_isb.sum(axis=0, skipna=True)["BDD test cases count"]
        total_bdd_others = queryset_release_other.sum(axis=0, skipna=True)["BDD test cases count"]

        data_bdd_per_story_isb.append(total_bdd_isb / total_us_islamabad if total_us_islamabad else None)
        data_bdd_per_story_other.append(total_bdd_others / total_us_others if total_us_others else None)

        data_us_comp_isb.append(total_us_points_islamabad / total_us_islamabad if total_us_islamabad else None)
        data_us_comp_other.append(total_us_points_others / total_us_others if total_us_others else None)

    dict_test_case_counts = {
        "datasets": [{
            "label": 'Pakistan Site',
            "data": data_us_comp_isb,
            "order": 2,
            "backgroundColor": '#2ecc71',
        },
            {
                "label": 'Other Sites',
                "data": data_us_comp_other,
                "order": 2,
                "backgroundColor": '#3498db',
            },
            {
                "label": 'BDD/US Pakistan Site',
                "data": data_bdd_per_story_isb,
                "type": 'line',
                "order": 1,
                "borderColor": "#e74c3c",
            },
            {
                "label": 'BDD/US Other Sites',
                "data": data_bdd_per_story_other,
                "type": 'line',
                "order": 1,
                "borderColor": "#e74c3c",
            }
        ],
        "labels": list_releases
    }
    return dict_test_case_counts


def get_all_releases(queryset: DataFrame):
    releases = []
    queryset.sort_values(by=["Release"])
    for row in queryset.iterrows():
        release = row[1].Release
        if not release in releases:
            releases.append(release)
    return releases
