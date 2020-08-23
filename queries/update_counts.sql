insert into hourly_counts (hashtag, hour, count)
values (%s,%s,%s)
on conflict (hashtag, hour)
do
    update set count = EXCLUDED.count + hourly_counts.count;