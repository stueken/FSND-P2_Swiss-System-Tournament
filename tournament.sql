-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the database for the tournament
-- create database tournament;

-- Create tables for the database
-- create table players (id serial, name text);
-- create table matches (id1 integer, id2 integer, winner integer, loser integer);

-- Populate players tables
-- insert into players (name) values ('Dagobert :)');
-- insert into players (name) values ('Donald :(');

-- Populate matches tables
-- INSERT INTO matches VALUES ('90','91','90','91');

-- View showing the wins for each player id also when never played
CREATE VIEW view_wins AS
SELECT players.id, count(matches.winner) AS wins 
FROM players LEFT JOIN matches 
ON players.id = matches.winner 
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