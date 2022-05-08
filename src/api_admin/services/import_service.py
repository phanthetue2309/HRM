import math
import re

import pandas
from api_base.services import BaseService
from api_user.models import User
from rest_framework.exceptions import ValidationError


class ExcelImportService(BaseService):
    """
    CHECK IMPORT METHOD
    """

    def __init__(self):
        self.rows = []
        self.valid_email = []
        self.invalid_email = []
        self.current_row = None
        self.status = []
        self.email = None
        self.name = None
        self.phone = None

    def check_import(self, df):
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        email_col = "email"
        name_col = "name"
        phone_col = "phone"
        for i in df.index:
            self.phone = None
            self.current_row = str(i + 2)
            self.email = str(df[email_col][i])
            self.name = str(df[name_col][i])

            if not isinstance(df[name_col][i], str):
                self.status.append("Invalid name")

            if (
                phone_col
                and re.search(r"\d{9,11}", str(df[phone_col][i]))
                and not math.isnan(int(df[phone_col][i]))
            ):
                self.phone = str(df[phone_col][i])
                self.status.append("Invalid phone format")

            if not (re.search(email_regex, self.email)):
                self.status.append("Invalid email format")
                self.append_status(email_list=self.invalid_email, success=False)
                continue
            existed = User.objects.filter(email=self.email).count()
            if existed:
                self.status.append("Already existed")
                self.append_status(email_list=self.invalid_email, success=False)
                continue
            if self.email in self.valid_email:
                self.status.append("Duplicate in file")
                self.append_status(email_list=self.invalid_email, success=False)
                continue
            self.status.append("Valid email")
            self.append_status(email_list=self.valid_email, success=True)
        return {
            "rows": self.rows,
            "valid": self.valid_email,
            "invalid": self.invalid_email,
        }

    def append_status(self, email_list, success):
        email_list.append(self.email)
        self.rows.append(
            {
                "row": self.current_row,
                "email": self.email,
                "name": self.name,
                "phone": self.phone,
                "status": self.status,
                "success": success,
            }
        )
        self.status = []

    @staticmethod
    def read_excel(file):
        try:
            return pandas.read_excel(file, engine="openpyxl")
        except Exception:
            raise ValidationError("Input file is not valid")
