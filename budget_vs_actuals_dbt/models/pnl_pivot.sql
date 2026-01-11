{{config(materialized='view')}}

with pnl_full as (
    select * from {{ref('pnl_full')}}
),

pnl_pivot as (
    select
        period,
        date,
        gl_id,
        gl_account,
        max(case when value_type_id = 1 then amount end) as actuals,
        max(case when value_type_id = 2 then amount end) as budget
    from pnl_full
    group by period,date, gl_id, gl_account
),

base_variances as (
    select
        period,
        date,
        gl_id,
        gl_account,
        actuals,
        budget,
        actuals - budget as variance
    from pnl_pivot
)

select
    period,
    date,
    gl_id,
    gl_account,
    actuals,
    budget,
    variance,
    COALESCE(variance / NULLIF(budget,0),0) as variance_pct
from base_variances
order by period, gl_id
