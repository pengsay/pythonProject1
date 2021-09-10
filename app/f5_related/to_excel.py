from openpyxl import load_workbook
from io import BytesIO as IO  # for modern python
import pandas as pd
from fastapi.responses import Response
from fastapi import HTTPException


def to_excel(data):
    output = IO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    s = pd.DataFrame(data)
    s.to_excel(writer, sheet_name="data")
    writer.save()
    output.seek(0)
    return Response(content=output.read(),
                    media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
