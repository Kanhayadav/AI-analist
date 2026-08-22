from .aliases import BUSINESS_ALIASES


def map_columns(df):

    mapping = {}

    unknown = []

    for column in df.columns:

        normalized = (
            column.lower()
            .replace("_", "")
            .replace(" ", "")
        )

        found = False

        for business_name, aliases in BUSINESS_ALIASES.items():

            if normalized in aliases:

                mapping[column] = business_name

                found = True

                break

        if not found:

            unknown.append(column)

    return mapping, unknown