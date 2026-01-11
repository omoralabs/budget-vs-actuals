{{config(materialized='view')}}

with pnl_comparison as (
    select * from {{ref('pnl_comparison')}}
),

base_variances as (
    select
        period,
        gl_account,
        budget,
        actuals - budget as variance
    from pnl_comparison
)

select
    period,
    gl_account,
    variance,
    COALESCE(variance / NULLIF(budget,0),0) as variance_pct
from base_variances
