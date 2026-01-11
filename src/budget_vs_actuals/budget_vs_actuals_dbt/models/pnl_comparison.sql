{{config(materialized='view')}}

with pnl_full as (
    select * from {{ref('pnl_full')}}
)


select
    period,
    gl_account,
    max(case when value_type_id = 1 then amount end) as actuals,
    max(case when value_type_id = 2 then amount end) as budget
from pnl_full
group by period, gl_account