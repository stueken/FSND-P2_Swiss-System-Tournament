#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math  # needed for log and ceil functions


# 1. Functions to meet requirements:

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament_extra")


def deleteMatches():
    """Remove all the match records from the database."""

    tournament = connect()
    cursor = tournament.cursor()
    cursor.execute("DELETE FROM matches")
    tournament.commit()
    tournament.close()


def deletePlayers():
    """Remove all the player records from the database."""

    tournament = connect()
    cursor = tournament.cursor()
    cursor.execute("DELETE FROM players")
    tournament.commit()
    tournament.close()


def countPlayers():
    """Returns the number of players currently registered."""

    tournament = connect()
    cursor = tournament.cursor()
    cursor.execute("""  SELECT count(*) AS count
                        FROM players """)
    # The cursor.fetchone() returns a tuple.
    # The count value is the first value of the tuple.
    return cursor.fetchone()[0]
    tournament.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    tournament = connect()
    cursor = tournament.cursor()
    cursor.execute("""  INSERT INTO players (name)
                        VALUES (%s) """, (name,))
    tournament.commit()
    tournament.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    tournament = connect()
    cursor = tournament.cursor()
    sql = ("""  SELECT players.id, players.name,
                       view_statistics_by_id.wins,
                       view_statistics_by_id.matches
                FROM players LEFT JOIN view_statistics_by_id
                ON players.id = view_statistics_by_id.id """)
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
    tournament.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    tournament = connect()
    cursor = tournament.cursor()
    cursor.execute("""  INSERT INTO matches (id1,id2)
                        VALUES (%s, %s) """, (winner, loser))
    tournament.commit()
    tournament.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    tournament = connect()
    cursor = tournament.cursor()

    # Get all ids and names sorted by number of wins
    cursor.execute(""" SELECT id, name FROM view_name_and_wins """)
    players_by_wins = cursor.fetchall()
    # players_by_wins:
    # [(id1, 'Twilight Sparkle'), (id3, 'Applejack'),
    #  (id2, 'Fluttershy'), (id4, 'Pinkie Pie')]

    # Building up two alternate lists using extended slices.
    # (https://docs.python.org/2.3/whatsnew/section-slices.html)
    next_round_winners = players_by_wins[::2]
    next_round_losers = players_by_wins[1::2]
    # next_round_winners: [(id1, 'Twilight Sparkle'), (id2, 'Fluttershy')]
    # next_round_losers: [(id3, 'Applejack'), (id4, 'Pinkie Pie')]

    # zip both lists together to receive a list of pairs of players for the
    # next round. (https://docs.python.org/2/library/functions.html#zip)
    next_round_pairings = zip(next_round_winners, next_round_losers)
    # next_round_pairings:
    # [((id1, 'Twilight Sparkle'), (id3, 'Applejack')),
    #  ((id2, 'Fluttershy'), (id4, 'Pinkie Pie'))]

    # As the return list should be formatted differently and tupels are
    # immutable, a new result_list is created with the same length, but
    # with the inner tupels concatenated.
    result_list = []
    for i in range(0, len(next_round_pairings)):
        result_list.append(
            next_round_pairings[i][0] + next_round_pairings[i][1])
    return result_list
    # result_list:
    # [(id1, 'Twilight Sparkle', id3, 'Applejack'),
    #  (id2, 'Fluttershy', id4, 'Pinkie Pie')]

    # BEGIN ALTERNATIVE APPROACH:
    # The below method was used for my first approach.
    # It is more complicated, but working as well to meet the requirments.
    # For that reason, I wanted to keep it for documenation reasons.

    # # Get all ids sorted by number of wins
    # cursor.execute(""" SELECT id FROM view_name_and_wins """)
    # players_by_wins = cursor.fetchall()

    # # Calculate the number of matches played
    # number_of_players = len(players_by_wins)
    # number_of_matches = number_of_players/2

    # # Insert adjacent players from the sorted id list into the matches table
    # # and delete them from the list until the the id list is empty (or number
    # # of matches is reached).
    # for i in range(0, number_of_matches):
    #     cursor.execute(
    #         """ INSERT INTO matches (id1,id2,winner)
    #         VALUES (%s, %s, %s) """, (players_by_wins[0][0],
    #                                   players_by_wins[1][0],
    #                                   players_by_wins[0][0]))
    #     tournament.commit()
    #     del players_by_wins[0:2]

    # # Adding the names to the ids from the players table
    # cursor.execute(
    #     """ SELECT matches.id1,
    #                (SELECT name FROM players WHERE players.id = matches.id1)
    #                AS name1,
    #                matches.id2,
    #                (SELECT name FROM players WHERE players.id = matches.id2)
    #                AS name2
    #         FROM matches""")
    # all_matches = cursor.fetchall()

    # Return only a list of players for the next round of the matches.
    # next_matches = all_matches[-number_of_matches:]
    # return next_matches
    # END ALTERNATIVE APPROACH

    tournament.close()


# 2. Functions for extra credit:


def deleteTournaments_extra():
    """Remove all tournament records from the database."""

    tournament = connect()
    cursor = tournament.cursor()
    cursor.execute("DELETE FROM tournament")
    tournament.commit()
    tournament.close()


def deleteTournamentPlayers_extra():
    """Remove all registered tournament players from the database."""

    tournament = connect()
    cursor = tournament.cursor()
    cursor.execute("DELETE FROM tournament_players")
    tournament.commit()
    tournament.close()


def registerTournament_extra(tournament_name):
    """Adds a tournament to the tournament database and returns its id.

    The database assigns a unique serial id number for the tournament.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      tournament_name: the tournament's name (need not be unique).

    Returns:
      the sequence number in the tid column of the tournament.
    """

    tournament = connect()
    cursor = tournament.cursor()

    # RETURNING returns the assigned sequence number of the tournament
    cursor.execute("""  INSERT INTO tournament (name)
                        VALUES (%s)
                        RETURNING tid """, (tournament_name,))
    tournament.commit()
    return cursor.fetchone()
    tournament.close()


def registerPlayersForTournament_extra(number_of_players):
    """Adds a specified number of players to the last registered
    tournament. To make it simple, it adds the specified number of players
    from the bottom of the table. Additionally, it returns the number of
    rounds, which should be played in the tournament.

    Args:
      number_of_players: number of players to be added to the tournament.

    Returns:
        rounds: number of rounds which should be played in the tournament.
    """

    tournament = connect()
    cursor = tournament.cursor()

    # Get the last registered tournament
    cursor.execute("""  SELECT tid FROM tournament
                        ORDER BY tid DESC LIMIT 1 """)
    tournament_id = cursor.fetchone()

    # Get the specified number of players from the end of the table in the
    # right order.
    cursor.execute("""  SELECT id
                        FROM (SELECT id
                              FROM players
                              ORDER BY id
                              DESC LIMIT (%s)) AS wrong_order
                        ORDER BY id """,
                   str(number_of_players))
    player_id = cursor.fetchall()

    # Register the players in the tournament_players table
    for i in range(0, len(player_id)):
        cursor.execute("""  INSERT INTO tournament_players (tid, pid, bye)
                        VALUES (%s, %s, %s) """,
                       (tournament_id, player_id[i], 'false'))
    tournament.commit()
    tournament.close()

    # log2(number_of_players) returns the number of rounds to be played. As
    # this can also be a floating number, math.ceil returns the smallest
    # integer value greater than or equal to number_of_players. This integer
    # number of rounds is being played.
    rounds = int(math.ceil(math.log(number_of_players, 2)))
    return rounds


def playerStandings_extra():
    """Returns a list of the players and their win and tie records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, ties, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        ties: the number of ties
        matches: the number of matches the player has played
    """

    tournament = connect()
    cursor = tournament.cursor()
    sql = ("""  SELECT players.id, players.name,
                       view_statistics_by_id_extra.wins,
                       view_statistics_by_id_extra.ties,
                       view_statistics_by_id_extra.matches
                FROM players LEFT JOIN view_statistics_by_id_extra
                ON players.id = view_statistics_by_id_extra.id """)
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
    tournament.close()


def playerStandings_last_tournament_extra():
    """Returns a list of the players and their win and tie records from the
    last tournament, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, ties, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won in the tournament
        ties: the number of matches the player has tied in the tournament
        matches: the number of matches the player has played in the tournament
    """

    tournament = connect()
    cursor = tournament.cursor()
    sql = ("""  SELECT players.id, players.name,
                       view_statistics_by_id_last_tournament_extra.wins,
                       view_statistics_by_id_last_tournament_extra.ties,
                       view_statistics_by_id_last_tournament_extra.matches
                FROM players
                RIGHT JOIN view_statistics_by_id_last_tournament_extra
                ON players.id = view_statistics_by_id_last_tournament_extra.pid """)
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
    tournament.close


def reportMatch_extra(winner, loser, tournament_id, tie):
    """Records the outcome of a single match between two players. However, if
    winner equals loser, the player doesn't doesn't play and gets a bye-win.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament_id:  the id of tournament the match is played in
      tie:  boolean variable telling if match should be a tie
    """

    tournament = connect()
    cursor = tournament.cursor()

    # if tie is not set (properly), its set to false
    if tie != 'true':
        tie = 'false'

    # if winner and loser are different, the match gets reported
    if winner != loser:
        cursor.execute("""  INSERT INTO matches (id1,id2,tie,tid)
                            VALUES (%s, %s, %s, %s) """,
                       (winner, loser, tie, tournament_id))

    # otherwise the player doesn't have an opponent, and uses his "bye-win"
    # without playing the match
    else:
        cursor.execute("""  UPDATE tournament_players set bye = true
                            WHERE tid = (%s) AND pid = (%s) """,
                       (tournament_id, winner))
    tournament.commit()
    tournament.close()


def swissPairings_extra():
    """Returns a list of pairs of players for the next round of a match.

    It doesn't matter if the number of players registered is even or uneven.
    Each player is paired with another player with an equal or nearly-equal win
    record, that is, a player adjacent to him or her in the standings.

    The player standings are ordered in the view:
        view_complete_statistics_last_tournament_extra
    according to wins (including bye-wins), ties and matches, whereby less
    matches are better.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    tournament = connect()
    cursor = tournament.cursor()

    # Get all ids and names sorted by number of wins
    cursor.execute(""" SELECT pid, name
                       FROM view_complete_statistics_last_tournament_extra """)
    players_by_wins = cursor.fetchall()
    # players_by_wins:
    # [(190, 'Al Bundy'), (184, 'Boba Fett'), (188, 'Mila Superstar'),
    #  (187, 'Captain Planet'), (186, 'Scooby Doo'), (189, 'Orko'),
    #  (185, 'Mr. T')]

    # if length of sorted list is uneven, add the last player to it again. This
    # will later result in a match against itselfs which gets properly handled
    # by the reportMatch_extra function.
    if len(players_by_wins) % 2 != 0:
        players_by_wins.append(players_by_wins[-1])
    # players_by_wins:
    # [(315, 'Boba Fett'), (316, 'Mr. T'), (317, 'Scooby Doo'), (318,
    #   'Captain Planet'), (319, 'Mila Superstar'), (320, 'Orko'), (321,
    #   'Al Bundy'), (321, 'Al Bundy')]

    # Building up two alternate lists using extended slices.
    # (https://docs.python.org/2.3/whatsnew/section-slices.html)
    next_round_winners = players_by_wins[::2]
    next_round_losers = players_by_wins[1::2]
    # next_round_winners: [(329, 'Boba Fett'), (331, 'Scooby Doo'), (333,
    #                       'Mila Superstar'), (335, 'Al Bundy')]
    # next_round_losers: [(330, 'Mr. T'), (332, 'Captain Planet'), (334,
    #                      'Orko'), (335, 'Al Bundy')]

    # zip both lists together to receive a list of pairs of players for the
    # next round. (https://docs.python.org/2/library/functions.html#zip)
    next_round_pairings = zip(next_round_winners, next_round_losers)
    # next_round_pairings:
    # [((329, 'Boba Fett'), (330, 'Mr. T')), ((331, 'Scooby Doo'), (332,
    #    'Captain Planet')), ((333, 'Mila Superstar'), (334, 'Orko')), ((335,
    #    'Al Bundy'), (335, 'Al Bundy'))]

    # As the return list should be formatted differently and tupels are
    # immutable, a new result_list is created with the same length, but
    # with the inner tupels concatenated.
    result_list = []
    for i in range(0, len(next_round_pairings)):
        result_list.append(
            next_round_pairings[i][0] + next_round_pairings[i][1])
    return result_list
    # result_list:
    # [(336, 'Boba Fett', 337, 'Mr. T'), (338, 'Scooby Doo', 339, 'Captain
    #   Planet'), (340, 'Mila Superstar', 341, 'Orko'), (342, 'Al Bundy', 342,
    #   'Al Bundy')]

    tournament.close()
