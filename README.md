```Python 3.10.2```
## Задание 1
Деплой: [sl-xone.herokuapp.com](https://sl-xone.herokuapp.com/)

## Задание 2
1.
```
SELECT bid.client_number, SUM(event_value.outcome = 'win') AS Побед, SUM(event_value.outcome = 'lose') AS Поражений 
FROM bid
JOIN event_value ON bid.play_id = event_value.play_id AND bid.coefficient = event_value.value
GROUP BY client_number;
```

2.
```
SELECT e.teams, count(*) AS game_count
FROM (SELECT concat(least(home_team, away_team), '-', greatest(home_team, away_team)) AS teams
FROM event_entity) AS e
GROUP BY teams
ORDER BY game_count;
```