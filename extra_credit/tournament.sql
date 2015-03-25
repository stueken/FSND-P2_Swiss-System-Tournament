-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the database for the tournament
CREATE DATABASE tournament_extra;

-- Create tables for the database
CREATE TABLE players (id serial, name text);
CREATE TABLE tournament (tid serial, name text);
CREATE TABLE tournament_players (tid integer, pid integer, bye boolean);
CREATE TABLE matches (id1 integer, id2 integer, tie boolean, tid integer);

-- Populate players tables
INSERT INTO players (name) VALUES ('Dagobert :)');
INSERT INTO players (name) VALUES ('Donald :(');

-- Populate tournament table
INSERT INTO tournament (name) VALUES ('World Cup'):

-- Populate matches tables
INSERT INTO matches VALUES ('22','23', true);
INSERT INTO matches VALUES ('24','25', false);
INSERT INTO matches VALUES ('26','27');


-- 1. Views to meet requirements

-- View showing the wins for each player id also when never played
CREATE VIEW view_wins AS
SELECT players.id, count(matches.id1) AS wins 
FROM players LEFT JOIN matches 
ON players.id = matches.id1 
GROUP BY players.id 
ORDER BY players.id;

-- View showing the matches for each player id also when never played
CREATE VIEW view_matches AS
SELECT players.id, count(matches.id1 + matches.id2) AS matches
FROM players LEFT JOIN matches
ON players.id = matches.id1 OR players.id = matches.id2
GROUP BY players.id;

-- View showing wins and matches for each player id sorted by id
CREATE VIEW view_statistics_by_id AS
SELECT view_wins.id, view_wins.wins, view_matches.matches
FROM view_wins RIGHT JOIN view_matches
ON view_wins.id = view_matches.id
ORDER BY view_matches.id;

-- View showing wins for each player id and name sorted by wins descending
CREATE VIEW view_name_and_wins AS
SELECT players.id, players.name, view_wins.wins
FROM players LEFT JOIN view_wins
ON players.id = view_wins.id
ORDER BY view_wins.wins DESC;


-- 2. Views for extra credit

-- View like view_wins, but not counting ties
-- COALESCE sets a value for NULL values
CREATE VIEW view_wins_extra AS
SELECT players.id, count(matches.id1) AS wins 
FROM players 
	LEFT JOIN matches 
	ON players.id = matches.id1 
	AND COALESCE(matches.tie, false) = false
GROUP BY players.id 
ORDER BY players.id;

-- View tid of the last registered tournament
CREATE VIEW view_get_last_tournament_extra AS
SELECT tid FROM tournament
ORDER BY tid DESC LIMIT 1;

-- View like view_ties_extra, but only regarding the last registered tournament via INNER JOIN
CREATE VIEW view_ties_last_tournament_extra AS
SELECT tournament_players.tid, tournament_players.pid, count(matches.id1 + matches.id2) AS ties
FROM tournament_players 
	LEFT JOIN matches 
	ON (tournament_players.pid = matches.id1 OR tournament_players.pid = matches.id2) AND matches.tie = true
	INNER JOIN view_get_last_tournament_extra ON tournament_players.tid = view_get_last_tournament_extra.tid
GROUP BY tournament_players.tid, tournament_players.pid
ORDER BY tournament_players.tid;

-- View like view_wins_extra, but only regarding the last registered tournament via INNER JOIN
CREATE VIEW view_wins_last_tournament_extra AS
SELECT tournament_players.tid, tournament_players.pid, count(matches.id1) AS wins 
FROM tournament_players 
	LEFT JOIN matches ON tournament_players.pid = matches.id1 AND COALESCE(matches.tie, false) = false
	INNER JOIN view_get_last_tournament_extra ON tournament_players.tid = view_get_last_tournament_extra.tid
GROUP BY tournament_players.tid, tournament_players.pid
ORDER BY tournament_players.tid;

-- View like view_wins_last_tournament_extra, but adding the bye-wins in the select clause
CREATE VIEW view_wins_with_byes_last_tournament_extra AS
SELECT tournament_players.tid, tournament_players.pid,
	   (count(matches.id1) + cast(tournament_players.bye AS int)) AS wins
FROM tournament_players 
	LEFT JOIN matches ON tournament_players.pid = matches.id1 AND COALESCE(matches.tie, false) = false
	INNER JOIN view_get_last_tournament_extra ON tournament_players.tid = view_get_last_tournament_extra.tid
GROUP BY tournament_players.tid, tournament_players.pid, tournament_players.bye
ORDER BY tournament_players.tid;

-- View showing ties for all player ids even though they don't have any tie.
CREATE VIEW view_ties_extra AS
SELECT players.id, count(matches.id1 + matches.id2) AS ties
FROM players LEFT JOIN matches 
ON (players.id = matches.id1 OR players.id = matches.id2) AND matches.tie = true
GROUP BY players.id
ORDER BY players.id;

-- View like view_matches, but only regarding the last registered tournament via INNER JOIN
CREATE VIEW view_matches_last_tournament_extra AS
SELECT tournament_players.tid, tournament_players.pid, count(matches.id1 + matches.id2) AS matches
FROM tournament_players 
	LEFT JOIN matches ON tournament_players.pid = matches.id1 OR tournament_players.pid = matches.id2
	INNER JOIN view_get_last_tournament_extra ON tournament_players.tid = view_get_last_tournament_extra.tid
GROUP BY tournament_players.tid, tournament_players.pid
ORDER BY tournament_players.tid, tournament_players.pid;

-- View like view_statistics_by_id, but adding ties
CREATE VIEW view_statistics_by_id_extra AS
SELECT view_wins_extra.id, view_wins_extra.wins, view_ties_extra.ties, view_matches.matches
FROM view_wins_extra
	LEFT JOIN view_matches ON view_wins_extra.id = view_matches.id
	LEFT JOIN view_ties_extra ON view_wins_extra.id = view_ties_extra.id
ORDER BY view_matches.id;

-- View like view_statistics_by_id_extra, but only regarding the last registered tournament via INNER JOIN
CREATE VIEW view_statistics_by_id_last_tournament_extra AS
SELECT view_wins_last_tournament_extra.tid, view_wins_last_tournament_extra.pid, 
	   view_wins_last_tournament_extra.wins, view_ties_last_tournament_extra.ties, 
	   view_matches_last_tournament_extra.matches
FROM view_wins_last_tournament_extra
	LEFT JOIN view_matches_last_tournament_extra 
		ON view_wins_last_tournament_extra.pid = view_matches_last_tournament_extra.pid
	LEFT JOIN view_ties_last_tournament_extra 
		ON view_wins_last_tournament_extra.pid = view_ties_last_tournament_extra.pid
ORDER BY view_matches_last_tournament_extra.pid;

-- View adding the byes as wins to view_statistics_by_id_last_tournament_extra
CREATE VIEW view_statistics_with_byes_last_tournament_extra AS
SELECT view_wins_with_byes_last_tournament_extra.tid, view_wins_with_byes_last_tournament_extra.pid, 
	   view_wins_with_byes_last_tournament_extra.wins, view_ties_last_tournament_extra.ties, 
	   view_matches_last_tournament_extra.matches
FROM view_wins_with_byes_last_tournament_extra
	LEFT JOIN view_matches_last_tournament_extra 
		ON view_wins_with_byes_last_tournament_extra.pid = view_matches_last_tournament_extra.pid
	LEFT JOIN view_ties_last_tournament_extra 
		ON view_wins_with_byes_last_tournament_extra.pid = view_ties_last_tournament_extra.pid
ORDER BY view_matches_last_tournament_extra.pid;

-- View of comprehensive tournament statistics adding the players name, and the 'bye'-indication to 
-- view_statistics_with_byes_last_tournament_extra. Sorting by 'bye' makes sure that player with
-- a bye get a match in the next round.
CREATE VIEW view_complete_statistics_last_tournament_extra AS
SELECT view_statistics_with_byes_last_tournament_extra.tid,
	   view_statistics_with_byes_last_tournament_extra.pid, 
   	   players.name,
	   view_statistics_with_byes_last_tournament_extra.wins,
	   view_statistics_with_byes_last_tournament_extra.ties, 
	   view_statistics_with_byes_last_tournament_extra.matches,
	   tournament_players.bye
FROM view_statistics_with_byes_last_tournament_extra
	LEFT JOIN players
		ON players.id = view_statistics_with_byes_last_tournament_extra.pid
	LEFT JOIN tournament_players
		ON tournament_players.tid = view_statistics_with_byes_last_tournament_extra.tid
		AND tournament_players.pid = view_statistics_with_byes_last_tournament_extra.pid
ORDER BY view_statistics_with_byes_last_tournament_extra.wins DESC, 
		 view_statistics_with_byes_last_tournament_extra.ties DESC,
		 tournament_players.bye DESC;
