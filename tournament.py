#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


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
                       view_statistics_by_id.wins, view_statistics_by_id.matches
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
