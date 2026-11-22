"""Demo of the database pipeline without a web server:  python demo_db.py"""
import json

import config, service
from database import init_db
from rank import rank_job

DB = config.BASE_DIR / "demo.db"
DB.unlink(missing_ok=True)
init_db(DB)

cfg = json.load(open(config.JOB_CONFIG_FILE))
job_id = service.create_job(cfg["title"], open(config.JOB_TEXT_FILE).read(), cfg["must_have"],
                            cfg["nice_to_have"], cfg["min_exp_years"], db_path=DB)
for f in sorted(config.RESUME_DIR.iterdir()):
    info = service.add_resume(f, db_path=DB)
    print("uploaded:", info["name"], info["skills"][:4])

print()
for r in rank_job(job_id, DB):
    print(f"#{r['rank']} {r['name']:<15} {r['score']:>5}  {r['decision']:<9} {r['reasons']['explanation']}")
