select
    row_number() over () as channel_key,
    channel_name,
    count(*) as total_posts,
    avg(view_count) as avg_views
from {{ ref('stg_telegram_messages') }}
group by channel_name
