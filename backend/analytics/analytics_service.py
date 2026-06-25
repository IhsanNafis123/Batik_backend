from collections import Counter
from datetime import datetime

from backend.config.database import supabase


class AnalyticsService:

    @staticmethod
    def get_dashboard_data():

        # ======================
        # USERS
        # ======================

        users = (
            supabase
            .table("users")
            .select("*")
            .execute()
        )

        # ======================
        # DESIGNS
        # ======================

        designs = (
            supabase
            .table("designs")
            .select("*")
            .execute()
        )

        # ======================
        # FITTINGS
        # ======================

        fittings = (
            supabase
            .table("fittings")
            .select("*")
            .execute()
        )

        total_users = len(users.data)
        total_designs = len(designs.data)
        total_fittings = len(fittings.data)

        # ======================
        # TOP MOTIF
        # ======================

        motif_counter = Counter()

        for design in designs.data:

            motif_counter[
                design["motif_name"]
            ] += 1

        if motif_counter:

            top_motif = motif_counter.most_common(1)[0][0]

        else:

            top_motif = "-"

        # ======================
        # DESIGN PER BULAN
        # ======================

        month_counter = {

            "Jan":0,
            "Feb":0,
            "Mar":0,
            "Apr":0,
            "Mei":0,
            "Jun":0,
            "Jul":0,
            "Agu":0,
            "Sep":0,
            "Okt":0,
            "Nov":0,
            "Des":0

        }

        bulan = [

            "Jan","Feb","Mar","Apr","Mei","Jun",

            "Jul","Agu","Sep","Okt","Nov","Des"

        ]

        for design in designs.data:

            if design["created_at"]:

                dt = datetime.fromisoformat(
                    design["created_at"]
                )

                month_counter[
                    bulan[
                        dt.month-1
                    ]
                ] += 1

        monthly_data = {

            "labels": list(month_counter.keys()),

            "values": list(month_counter.values())

        }

        # ======================
        # TOP MOTIF CHART
        # ======================

        top5 = motif_counter.most_common(5)

        motif_chart = {

            "labels":[

                x[0]

                for x in top5

            ],

            "values":[

                x[1]

                for x in top5

            ]

        }

        # ======================
        # MODE
        # ======================

        mode_counter = Counter()

        for design in designs.data:

            mode_counter[
                design["mode"]
            ] += 1

        mode_chart = {

            "labels":

            list(

                mode_counter.keys()

            ),

            "values":

            list(

                mode_counter.values()

            )

        }

        # ======================
        # TOP USER
        # ======================

        creator_counter = Counter()

        for design in designs.data:

            creator_counter[
                design["user_id"]
            ] += 1

        creator_chart = {

            "labels":[

                f"User {x[0]}"

                for x

                in creator_counter.most_common(5)

            ],

            "values":[

                x[1]

                for x

                in creator_counter.most_common(5)

            ]

        }

        return {

            "total_users": total_users,

            "total_designs": total_designs,

            "total_fittings": total_fittings,

            "top_motif": top_motif,

            "monthly_chart": monthly_data,

            "motif_chart": motif_chart,

            "mode_chart": mode_chart,

            "creator_chart": creator_chart

        }