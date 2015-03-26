#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


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
    print " "
    print "---------------------------------"
    print "Start of 8E - testPairings_extra."
    print " "

    # deleteMatches()
    # deletePlayers()
    # deleteTournaments_extra()
    # deleteTournamentPlayers_extra()

    # register a new tournament and save returned tid in a temporary variable
    tid = registerTournament_extra("Master of the Mysterious Seven")[0]
    print "New Tournamenent registered with Tournament id (tid) " + str(tid)

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
    print "9 new players have been registered in the database."

    # add the last 7 players to the last registered tournament
    registerPlayersForTournament_extra(7)
    standings = playerStandings_last_tournament_extra()
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]
    print ("7 players have been sucessfully registered for the "
           "tournament " + str(tid) + ".")

    # report the first round matches including ties, bye-wins, and missing
    # inputfor tie.
    reportMatch_extra(id1, id2, tid, 'false')
    print "Match 1 reported a winner."
    reportMatch_extra(id3, id4, tid, 'true')
    print "Match 2 reported a tie."
    reportMatch_extra(id5, id6, tid, '')
    print "Match 3 reported a winnen, even though the tie input wasn't clear."
    # the odd player gets a "bye" when played against himself
    reportMatch_extra(id7, id7, tid, '')
    print "The remaining odd player gets his free bye-win."

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
    print "Pairings for round 2:"
    print pairings

    print " "
    print ("End of 8E - testPairings_extra sucessfully finished. After one "
           "match, players with similar amount of wins (+-1) are paired.")
    print "---------------------------------"
    print " "


def testPlayTournament_extra():
    """ A whole sample tournament with an unenven amount of players (7) is
    played through. The amount of rounds to be played gets calculated when
    an amount of players gets registered for a tournament.

    Note: Each pairing and the player standings are documented for each round
    in the comments.
    """
    print " "
    print "---------------------------------------"
    print "Start of 9E - testPlayTournament_extra."
    print " "

    tid = registerTournament_extra("Master of the Mysterious Seven")[0]
    print "New Tournamenent registered with Tournament id (tid) " + str(tid)

    registerPlayer("Boba Fett")
    registerPlayer("Mr. T")
    registerPlayer("Scooby Doo")
    registerPlayer("Captain Planet")
    registerPlayer("Mila Superstar")
    registerPlayer("Orko")
    registerPlayer("Al Bundy")
    rounds = registerPlayersForTournament_extra(7)
    print ("7 new players have been registered in the database and for the "
           "tournament" + str(tid) + ".")
    print str(rounds) + " are going to be played in the tournament."

    # There are 3 rounds with 7 players
    for i in range(0, rounds):
        pairings = swissPairings_extra()
        print " "
        print "pairings for round " + str(i + 1) + ":"
        print pairings
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
        print "The results are:"
        match_number = 1
        for pairing in pairings:
            reportMatch_extra(pairing[0], pairing[2], tid, 'false')
            if pairing[0] != pairing[2]:
                print ("Round " + str(i + 1) + " Match " + str(match_number) +
                       " - Winner: " + str(pairing[1]))
            else:
                print (str(pairing[1]) + " doesn't play and gets a free "
                       "bye-win.")
            match_number += 1

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

    print " "
    print ("End of 9E - testPlayTournament_extra sucessfully finished. "
           "Tournament with uneven amount of players played through.")
    print "---------------------------------------"
    print " "


if __name__ == '__main__':
    """NOTE: After implementing foreign key not-null constraints, the delete
    functions would need to get a more complex logic. However, as those are not
    needed for the new database model to function, this is not done. Therefore
    only the last functions are used to demonstrate the working database model.
    """

    # Test cases for meet for extra credit
    testPairings_extra()
    testPlayTournament_extra()
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!! Success!  All extra tests pass to exceed specifications !!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print " "
