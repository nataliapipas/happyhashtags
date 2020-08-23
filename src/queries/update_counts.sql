insert into hourly_counts (hashtag, hour, count)
values ('h1','2020-01-01 00:00:00', 3)
on conflict (hashtag, hour)
do
    update set count = EXCLUDED.count + hourly_counts.count;
