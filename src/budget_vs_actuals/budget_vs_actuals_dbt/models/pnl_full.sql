{{config(materialised='view')}}

with pnl_rollup as (
    select * from {{ref('pnl_rollup')}}
),

periods as (
    select * from {{source('budget_vs_actuals', 'periods')}}
),

gl_accounts as (
    select * from {{source('budget_vs_actuals', 'gl_accounts')}}
),

value_types as (
    select * from {{source('budget_vs_actuals', 'value_types')}}
)

select
    p.period,
    ga.name as gl_account,
    pnlr.value_type_id,
    vt.name as type,
    pnlr.amount
from pnl_rollup pnlr
join periods p ON p.id = pnlr.period_id
join gl_accounts ga ON ga.id = pnlr.gl_account_id
join value_types vt ON vt.id = pnlr.value_type_id
