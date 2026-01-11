{{config(materialized='view')}}

WITH RECURSIVE pnl as (
    select * from {{source('financial_data', 'pnl')}}
),

gl_accounts as (
    select * from {{source('financial_data', 'gl_accounts')}}
),

pnl_rollup as (
    select
        period_id,
        gl_account_id,
        value_type_id,
        amount,
        0 as level
    from pnl

    union all

    select
        pr.period_id,
        ga.parent_gl as gl_account_id,
        pr.value_type_id,
        pr.amount,
        pr.level + 1
    from pnl_rollup pr
    join gl_accounts ga on ga.id = pr.gl_account_id
    join gl_accounts parent_ga on parent_ga.id = ga.parent_gl
    where ga.parent_gl is not null
)

select
    period_id,
    gl_account_id,
    value_type_id,
    sum(amount) as amount
from pnl_rollup
group by period_id, gl_account_id, value_type_id
order by period_id, value_type_id, gl_account_id
