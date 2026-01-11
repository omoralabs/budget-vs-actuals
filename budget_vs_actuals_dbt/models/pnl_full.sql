{{config(materialised='view')}}

with pnl_base_data as (
    select * from {{ref('pnl_base_data')}}
),

base_and_gross as (
    select * from pnl_base_data

    UNION ALL

    select
        period,
        date,
        3000 as gl_id,
        'gross_margin' as gl_account,
        value_type_id,
        type,
        sum(case when gl_id = 1000 then amount else 0 end) - sum(case when gl_id = 2000 then amount else 0 end) as amount
    from pnl_base_data
    group by period, date, value_type_id, type

    UNION ALL

    select
        period,
        date,
        7000 as gl_id,
        'total_cost' as gl_account,
        value_type_id,
        type,
        sum(case when gl_id = 2000 then amount else 0 end) + sum(case when gl_id = 4000 then amount else 0 end) + sum(case when gl_id = 6000 then amount else 0 end)
    from pnl_base_data
    group by period, date, value_type_id, type
),

base_and_gross_and_contribution as (
    select * from base_and_gross

    UNION ALL

    select
        period,
        date,
        5000 as gl_id,
        'contribution_margin' as gl_account,
        value_type_id,
        type,
        sum(case when gl_id = 3000 then amount else 0 end) - sum(case when gl_id = 4000 then amount else 0 end) as amount
    from base_and_gross
    group by period, date, value_type_id, type

    UNION ALL

    select
        period,
        date,
        3001 as gl_id,
        'gross_margin_pct' as gl_account,
        value_type_id,
        type,
        COALESCE(sum(case when gl_id = 3000 then amount else 0 end) / nullif(sum(case when gl_id = 1000 then amount else 0 end),0),0) as amount
    from base_and_gross
    group by period, date, value_type_id, type

    UNION ALL

    select
        period,
        date,
        7001 as gl_id,
        'total_cost_pct' as gl_account,
        value_type_id,
        type,
        COALESCE(sum(case when gl_id = 7000 then amount else 0 end) / nullif(sum(case when gl_id = 1000 then amount else 0 end),0),0) as amount
    from base_and_gross
    group by period, date, value_type_id, type


    UNION ALL

    select
        period,
        date,
        2001 as gl_id,
        'cogs_pct' as gl_account,
        value_type_id,
        type,
        COALESCE(sum(case when gl_id = 2000 then amount else 0 end) / nullif(sum(case when gl_id = 1000 then amount else 0 end),0),0) as amount
    from base_and_gross
    group by period, date, value_type_id, type

    UNION ALL

    select
        period,
        date,
        4001 as gl_id,
        'commercial_costs_pct' as gl_account,
        value_type_id,
        type,
        COALESCE(sum(case when gl_id = 4000 then amount else 0 end) / nullif(sum(case when gl_id = 1000 then amount else 0 end),0),0) as amount
    from base_and_gross
    group by period, date, value_type_id, type

    UNION ALL

    select
        period,
        date,
        6001 as gl_id,
        'fixed_costs_pct' as gl_account,
        value_type_id,
        type,
        COALESCE(sum(case when gl_id = 6000 then amount else 0 end) / nullif(sum(case when gl_id = 1000 then amount else 0 end),0),0) as amount
    from base_and_gross
    group by period, date, value_type_id, type
),

base_ebitda as (

    select * from base_and_gross_and_contribution

    UNION ALL

    select
        period,
        date,
        8000 as gl_id,
        'ebitda' as gl_account,
        value_type_id,
        type,
        sum(case when gl_id = 5000 then amount else 0 end) - sum(case when gl_id = 6000 then amount else 0 end) as amount
    from base_and_gross_and_contribution
    group by period, date, value_type_id, type

    UNION ALL

    select
        period,
        date,
        5001 as gl_id,
        'contribution_margin_pct' as gl_account,
        value_type_id,
        type,
        COALESCE(sum(case when gl_id = 5000 then amount else 0 end) / nullif(sum(case when gl_id = 1000 then amount else 0 end),0),0) as amount
    from base_and_gross_and_contribution
    group by period, date, value_type_id, type
)

select * from base_ebitda

UNION ALL

select
    period,
    date,
    8001 as gl_id,
    'ebitda_pct' as gl_account,
    value_type_id,
    type,
    COALESCE(sum(case when gl_id = 8000 then amount else 0 end) / nullif(sum(case when gl_id = 1000 then amount else 0 end),0),0) as amount
from base_ebitda
group by period, date, value_type_id, type
order by gl_id, value_type_id, period, date
