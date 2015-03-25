#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even "
                         "before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches played.")
    print ("6. Newly registered players appear in the standings with no "
           "matches.")


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins "
                             "recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testDeleteTournaments_extra():
    deleteMatches()
    deletePlayers()
    deleteTournaments_extra()
    print "2E. Tournament records can be deleted."


def testRegisterCountDelete_extra():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    registerPlayer("Boba Fett")
    registerPlayer("Mr. T")
    registerPlayer("Scooby Doo")
    c = countPlayers()
    if c != 7:
        raise ValueError(
            "After registering seven players, countPlayers should be 7.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5E. Odd amount of players can be registered and deleted."


def testStandingsBeforeMatches_extra():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    registerPlayer("Boba Fett")
    registerPlayer("Mr. T")
    registerPlayer("Scooby Doo")
    registerPlayer("Orko")
    registerPlayer("Al Bundy")
    standings = playerStandings()
    if len(standings) < 7:
        raise ValueError("Players should appear in playerStandings even "
                         "before they have played any matches.")
    elif len(standings) > 7:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2),
     (id3, name3, wins3, matches3), (id4, name4, wins4, matches4),
     (id5, name5, wins5, matches5), (id6, name6, wins6, matches6),
     (id7, name7, wins7, matches7)] = standings
    if (matches1 != 0 or matches2 != 0 or matches3 != 0 or matches4 != 0 or
        matches5 != 0 or matches6 != 0 or matches7 != 0 or wins1 != 0 or
        wins2 != 0 or wins3 != 0 or wins4 != 0 or wins5 != 0 or wins6 != 0 or
            wins1 != 0):
                raise ValueError(
                    "Newly registered players should have no matches or wins.")
    if set([name1, name2, name3, name4, name5, name6, name7]) != set([
            "Melpomene Murray", "Randy Schwartz", "Boba Fett", "Mr. T",
            "Scooby Doo", "Orko", "Al Bundy"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches played.")
    print ("6E. Uneven amount of newly registered players appear in the "
           "standings with no matches.")


def testReportMatches_extra():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Scooby Doo")
    registerPlayer("Orko")
    registerPlayer("Al Bundy")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id7)  # the odd player gets a "bye"
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if len(standings) % 2 == 0:  # number of players dividable by 2
            if m != 1:
                raise ValueError("Each player should have one match recorded.")
            if i in (id1, id3) and w != 1:
                raise ValueError("Each winner should have one win recorded.")
            elif i in (id2, id4) and w != 0:
                raise ValueError("Each loser should have zero wins "
                                 "recorded.")
        else:  # odd number of players
            if i in (id1, id3, id5, id7) and w != 1:
                raise ValueError("Each winner should have one win recorded.")
            elif i in (id2, id4, id6) and w != 0:
                raise ValueError("Each loser should have zero wins "
                                 "recorded.")
    print ("7E. After a match, players have updated standings. Players who "
           "didn't play get a bye-win.")


def testPairings_extra():
    """ Some extra featues which are testing in this function:

    1. Uneven amount of registered players (9)
    2. Uneven amount of players registered for a tournament (7)
    3. When there is an uneven amount of players, the not matched player gets
       a 'bye-win'. Each player can only get a one bye-win in a tournament.
    4. A match can be reported as a tie
    5. Matches or players don't need to be deleted as multiple tournaments
       are possible and players need to be registered for each tournament
       separately.
    """

    # deleteMatches()
    # deletePlayers()
    deleteTournaments_extra()
    deleteTournamentPlayers_extra()

    # register a new tournament and save returned tid in a temporary variable
    tid = registerTournament_extra("Master of the Mysterious Seven")[0]

    # register 9 players (not for the tournament yet)
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Boba Fett")
    registerPlayer("Mr. T")
    registerPlayer("Scooby Doo")
    registerPlayer("Captain Planet")
    registerPlayer("Mila Superstar")
    registerPlayer("Orko")
    registerPlayer("Al Bundy")

    # add the last 7 players to the last registered tournament
    registerPlayersForTournament_extra(7)
    standings = playerStandings_last_tournament_extra()
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]

    # report the first round matches including ties, bye-wins, and missing
    # inputfor tie.
    reportMatch_extra(id1, id2, tid, 'false')
    reportMatch_extra(id3, id4, tid, 'true')
    reportMatch_extra(id5, id6, tid, '')
    # the odd player gets a "bye" when played against himself
    reportMatch_extra(id7, id7, tid, '')

    # if odd number of players, swissPairings creates a match against itself
    # for the last player - reportMatch_extra recognizes this and reports a
    # 'bye' for this player.
    pairings = swissPairings_extra()
    if len(pairings) != 4:
        raise ValueError(
            "For seven players, swissPairings should return four pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6), (pid7, pname7, pid7, pname7)] = pairings
    correct_pairs = set([frozenset([id7, id1]), frozenset([id5, id4]),
                         frozenset([id3, id6]), frozenset([id2, id2])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]),
                        frozenset([pid5, pid6]), frozenset([pid7, pid7])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with similar amount of wins and ties"
            "should be paired. Thereby those with less matches should be"
            "pulled first (only one bye-win for each player).")

    # results after one round with an uneven amount of players an a tie:
    # --> select * from view_complete_statistics_last_tournament_extra;
    #  tid | pid |      name      | wins | ties | matches | bye
    # -----+-----+----------------+------+------+---------+-----
    #   84 | 560 | Al Bundy       |    1 |    0 |       0 | t
    #   84 | 554 | Boba Fett      |    1 |    0 |       1 | f
    #   84 | 558 | Mila Superstar |    1 |    0 |       1 | f
    #   84 | 557 | Captain Planet |    0 |    1 |       1 | f
    #   84 | 556 | Scooby Doo     |    0 |    1 |       1 | f
    #   84 | 559 | Orko           |    0 |    0 |       1 | f
    #   84 | 555 | Mr. T          |    0 |    0 |       1 | f
    # (7 rows)

    print ("8E. After one match, players with similar amount of wins (+-1) "
           "are paired.")


def testPlayTournament_extra():
    """ A whole sample tournament with an unenven amount of players (7) is
    played through. The amount of rounds to be played gets calculated when
    an amount of players gets registered for a tournament.

    Note: Each pairing and the player standings are documented for each round
    in the comments.
    """

    tid = registerTournament_extra("Master of the Mysterious Seven")[0]
    registerPlayer("Boba Fett")
    registerPlayer("Mr. T")
    registerPlayer("Scooby Doo")
    registerPlayer("Captain Planet")
    registerPlayer("Mila Superstar")
    registerPlayer("Orko")
    registerPlayer("Al Bundy")
    rounds = registerPlayersForTournament_extra(7)

    # There are 3 rounds with 7 players
    for i in range(0, rounds):
        pairings = swissPairings_extra()
        # 1st pairings:
        # [(438, 'Boba Fett', 439, 'Mr. T'), (440, 'Scooby Doo', 441, 'Captain
        #   Planet'), (442, 'Mila Superstar', 443, 'Orko'), (444, 'Al Bundy',
        #   444, 'Al Bundy')]
        #
        # 2nd pairings:
        # [(444, 'Al Bundy', 442, 'Mila Superstar'), (440, 'Scooby Doo', 438,
        #   'Boba Fett'), (441, 'Captain Planet', 439, 'Mr. T'), (443, 'Orko',
        #   443, 'Orko')]
        #
        # 3rd pairing:
        # [(444, 'Al Bundy', 440, 'Scooby Doo'), (443, 'Orko', 441, 'Captain
        #   Planet'), (438, 'Boba Fett', 442, 'Mila Superstar'), (439, 'Mr. T',
        #   439, 'Mr. T')]

        # generate match outcomes for all pairings. To make it quick, ties are
        # set to false.
        for pairing in pairings:
            reportMatch_extra(pairing[0], pairing[2], tid, 'false')
        # --> select * from view_complete_statistics_last_tournament_extra;
        # 1st round:
        #  tid | pid |      name      | wins | ties | matches | bye
        # -----+-----+----------------+------+------+---------+-----
        #   67 | 444 | Al Bundy       |    1 |    0 |       0 | t
        #   67 | 442 | Mila Superstar |    1 |    0 |       1 | f
        #   67 | 440 | Scooby Doo     |    1 |    0 |       1 | f
        #   67 | 438 | Boba Fett      |    1 |    0 |       1 | f
        #   67 | 441 | Captain Planet |    0 |    0 |       1 | f
        #   67 | 439 | Mr. T          |    0 |    0 |       1 | f
        #   67 | 443 | Orko           |    0 |    0 |       1 | f
        #
        # 2nd round:
        #  tid | pid |      name      | wins | ties | matches | bye
        # -----+-----+----------------+------+------+---------+-----
        #   67 | 444 | Al Bundy       |    2 |    0 |       1 | t
        #   67 | 440 | Scooby Doo     |    2 |    0 |       2 | f
        #   67 | 443 | Orko           |    1 |    0 |       1 | t
        #   67 | 441 | Captain Planet |    1 |    0 |       2 | f
        #   67 | 438 | Boba Fett      |    1 |    0 |       2 | f
        #   67 | 442 | Mila Superstar |    1 |    0 |       2 | f
        #   67 | 439 | Mr. T          |    0 |    0 |       2 | f
        #
        # 3rd round:
        #  tid | pid |      name      | wins | ties | matches | bye
        # -----+-----+----------------+------+------+---------+-----
        #   67 | 444 | Al Bundy       |    3 |    0 |       2 | t
        #   67 | 443 | Orko           |    2 |    0 |       2 | t
        #   67 | 440 | Scooby Doo     |    2 |    0 |       3 | f
        #   67 | 438 | Boba Fett      |    2 |    0 |       3 | f
        #   67 | 439 | Mr. T          |    1 |    0 |       2 | t
        #   67 | 441 | Captain Planet |    1 |    0 |       3 | f
        #   67 | 442 | Mila Superstar |    1 |    0 |       3 | f

    print ("9E. Tournament with uneven amount of players played through.")

if __name__ == '__main__':
    # Test cases to meet project requirements
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass to meet specifications!"

    # Test cases for meet for extra credit
    testDeleteTournaments_extra()
    testRegisterCountDelete_extra()
    testStandingsBeforeMatches_extra()
    testReportMatches_extra()
    testPairings_extra()
    testPlayTournament_extra()
    print "Success!  All extra tests pass to exceed specifications!"
