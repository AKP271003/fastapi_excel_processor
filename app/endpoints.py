from fastapi import APIRouter, Query, HTTPException
from .parser import TABLES_CACHE, get_table_matches

router = APIRouter()

@router.get("/list_tables")
def list_tables():
    """List all unique table names present in the Excel sheet."""
    return {"tables": list(TABLES_CACHE.keys())}

@router.get("/get_table_details")
def get_table_details(table_name: str = Query(..., description="Name of the table")):
    """Return the row names for the selected table."""
    matches = get_table_matches(table_name)
    if not matches:
        raise HTTPException(status_code=404, detail="Table not found")
    tinfo = TABLES_CACHE[matches[0]][0]
    return {"table_name": matches[0], "row_names": tinfo['row_headings']}

@router.get("/row_sum")
def row_sum(
    table_name: str = Query(..., description="Name of the table"),
    row_name: str = Query(..., description="Name of the row")
):
    """Calculate and return the sum of all numerical data points in the row."""
    matches = get_table_matches(table_name)
    if not matches:
        raise HTTPException(status_code=404, detail="Table not found")
    tinfo = TABLES_CACHE[matches[0]][0]
    found = False
    for heading, values in tinfo['content'].items():
        if heading.strip().lower() == row_name.strip().lower():
            found = True
            total = 0.0
            for v in values:
                if isinstance(v, str) and v.endswith('%'):
                    try:
                        total += float(v.rstrip('%'))
                    except ValueError:
                        pass
                else:
                    try:
                        total += float(v)
                    except ValueError:
                        pass
            return {
                "table_name": matches[0],
                "row_name": heading,
                "sum": total
            }
    if not found:
        raise HTTPException(status_code=404, detail="Row not found in the specified table")
