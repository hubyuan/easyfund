import xalpha as xa
from sqlalchemy import create_engine

# engine = create_engine('mysql://root:password@127.0.0.1/database?charset=utf8')
io = {"save": True, "fetch": True, "form": "csv", "path": "test/"}
xa.fundinfo("510018", **io)