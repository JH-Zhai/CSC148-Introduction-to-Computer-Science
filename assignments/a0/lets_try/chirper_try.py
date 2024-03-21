"""CSC148 Assignment 0

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains the starter code for Assignment 0.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""

from __future__ import annotations
from typing import List, Dict, TextIO, Optional
from datetime import datetime

CHEEP_LENGTH = 100
SENTINEL = 'END_REPLIES'


class Cheep:
    """A class to represent a cheep.

    === Public Attributes ===
    user: The user who wrote this cheep
    date: The day and time this cheep was posted

    === Private Attributes
    _text: The text of the cheep
    _replies: cheeps that are a reply to this cheep

    === Representation Invariants ===
    - len(_text) <= CHEEP_LENGTH
    - _replies is sorted in ascending chronological order and contains only
    cheeps that are newer than this cheep
    """

    user: str
    date: datetime
    _text: str
    _replies: List[Cheep]

    def __init__(self, user: str, text: str, date: datetime = None) -> None:
        """Initialize this cheep to have username <user>, text <text>, and date
        <date>, with empty replies.
        If no date is provided, use the current date and time.
        Text should be truncated to a maximum of CHEEP_LENGTH characters.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c1.user
        'UofT'
        >>> c1._text
        'Happy back to school!'
        >>> c1.date
        datetime.datetime(2019, 9, 5, 9, 1)
        >>> c2 = Cheep('someone', 'A' * (CHEEP_LENGTH - 1) + 'B' * 100)
        >>> c2._text == 'A' * (CHEEP_LENGTH - 1) + 'B'
        True
        """
        self._replies = []
        self.user = user
        if len(text) > CHEEP_LENGTH:
            self._text = (text[:CHEEP_LENGTH])
        else:
            self._text = text
        if date is None:
            self.date = datetime.now()
        else:
            self.date = date

    def add_reply(self, reply: Cheep) -> None:
        """Add <reply> to the replies for this cheep, if reply was posted at a
        later date. Otherwise, do not add to replies.

        Replies must be added in chronological order.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First class!', \
        datetime(2019, 9, 5, 11, 1, 0))
        >>> c1.add_reply(c2)
        >>> len(c1._replies)
        1
        >>> t3 = Cheep('a_student', 'Setting my alarm!', \
        datetime(2019, 9, 4, 22, 30, 0))
        >>> c1.add_reply(t3)
        >>> len(c1._replies)
        1
        """
        if self.date >= reply.date:
            return None

        if len(self._replies) == 0:
            self._replies.append(reply)
            return None

        if reply.date > self._replies[len(self._replies) - 1].date:
            self._replies.append(reply)
            return None

        for cheep in self._replies:
            if reply.date < cheep.date:
                self._replies.insert(self._replies.index(cheep), reply)
                break
        return None

    def get_repliers(self) -> List[str]:
        """Return a list of users (including duplicates) that replied to
        this cheep, in the order they appear.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> t3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> c1.add_reply(t3)
        >>> c4 = Cheep('prof_smith', 'Prepping my lecture', \
        datetime(2019, 9 ,6))
        >>> c1.add_reply(c4)
        >>> c1.get_repliers()
        ['prof_smith', 'a_student', 'a_student']
        """
        repliername = []
        for cheep in self._replies:
            repliername.append(cheep.user)
        return repliername

    def __contains__(self, keyword: str) -> bool:
        """Return True iff <keyword> is contained in the text of this cheep.

        >>> c1 = Cheep('user1', 'I love cats!')
        >>> 'cat' in c1
        True
        >>> c2 = Cheep('user1', 'A' * CHEEP_LENGTH + 'I love cats!')
        >>> 'cat' in c2
        False
        """
        return keyword in self._text

    def __str__(self) -> str:
        """Return the string representation of this cheep.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> t3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> c1.add_reply(t3)
        >>> c4 = Cheep('prof_smith', 'Prepping my lecture', \
        datetime(2019, 9 ,6))
        >>> c1.add_reply(c4)
        >>> print(c1)
        UofT said: Happy back to school!
        prof_smith replied: Prepping my lecture
        a_student replied: Weekend!!
        a_student replied: First CSC148 lecture!
        """
        stringrepresentation = self.user + ' said: ' + self._text
        for reply in self._replies:
            stringrepresentation = stringrepresentation + '\n' + \
                                   reply.user + ' replied: ' + reply._text
        return stringrepresentation


class Chirper:
    """A class to represent our social media platform Chirper.

    === Private Attributes ===
    _cheeps: The cheeps in this Chirper instance
    """
    _cheeps: List[Cheep]

    def __init__(self) -> None:
        """Initialize this Chirper to have no cheeps.

        >>> chirper = Chirper()
        >>> len(chirper._cheeps)
        0
        """
        self._cheeps = []

    def post_cheep(self, new_cheep: Cheep) -> None:
        """Add the cheep <new_cheep> to this Chirper.

        >>> c1 = Cheep('UofT', 'Happy back to school!', datetime(2019, 9, 5))
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> len(chirper._cheeps)
        1
        """
        self._cheeps.append(new_cheep)

    def cheeps_by_year(self) -> Dict[int, List[Cheep]]:
        """Return a dictionary with keys as the years for cheeps in this
        Chirper, and values are the cheeps from that year.

        Years for which there are no cheeps should not appear in the dictionary.

        >>> c1 = Cheep('UofT', 'Happy back to school!', datetime(2019, 9, 5))
        >>> c2 = Cheep('a_user', 'I love summer', datetime(2019, 7, 15))
        >>> t3 = Cheep('user2', 'Pancakes or waffles?', datetime(2017, 5, 15))
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> chirper.post_cheep(c2)
        >>> chirper.post_cheep(t3)
        >>> chirper.cheeps_by_year() == {2019: [c1, c2], 2017: [t3]}
        True
        """
        newdict = {}
        for cheep in self._cheeps:
            if cheep.date.year not in newdict.keys():
                newdict[cheep.date.year] = [cheep]
            else:
                newdict[cheep.date.year].append(cheep)
        return newdict

    def read_cheeps(self, f: TextIO) -> None:
        """Read in cheeps from a text file <f>. Every cheep should be stored in
        this Chirper, and cheeps that are replies should also be added to
        the reply list of the cheep they reply to.

        Each line in the file is formatted as:
        user,cheep_text,year,month,day,hour,minute,second
        OR
        a sentinel denoting the end of replies to a cheep, ie. SENTINEL

        There are no commas other than those separating data.
        year to second are all just digits.

        For simplicity, we will assume that reply chirps cannot have their own
        replies.

        Note: no docstring examples for functions or methods that do file IO.
        """
        # with open('cheep_data.txt') as f:
        lines = f.read().splitlines()
        end = True
        firstcheeps = []
        for line in lines:
            if line.startswith(SENTINEL):
                end = True
            else:
                if not end:
                    a = line.split(',')
                    replycheep = Cheep(a[0], a[1],
                                       datetime(int(a[2]), int(a[3]), int(a[4]),
                                                int(a[5]), int(a[6]),
                                                int(a[7])))
                    self.post_cheep(replycheep)
                    firstcheeps[len(firstcheeps) - 1].add_reply(replycheep)
                if end:
                    a = line.split(',')
                    thefirstcheep = Cheep(a[0], a[1],
                                          datetime(int(a[2]), int(a[3]),
                                                   int(a[4]), int(a[5]),
                                                   int(a[6]), int(a[7])))
                    firstcheeps.append(thefirstcheep)
                    self.post_cheep(thefirstcheep)
                    end = False

    def most_popular_cheep(self) -> Optional[Cheep]:
        """Return the cheep with the most replies, or None if there are no
        cheeps.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> t3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> chirper.post_cheep(c2)
        >>> chirper.post_cheep(t3)
        >>> chirper.most_popular_cheep() == c1
        True
        """
        if not self._cheeps:
            return None

        listofcheeps = self._cheeps.copy()
        for i in range(len(listofcheeps)):
            for j in range(0, (len(listofcheeps) - i - 1)):
                if len(listofcheeps[j].get_repliers()) > len(
                        listofcheeps[j + 1].get_repliers()):
                    listofcheeps[j], listofcheeps[j + 1] = \
                        listofcheeps[j + 1], listofcheeps[j]
        return listofcheeps[len(listofcheeps) - 1]

    def find_fan(self, user: str) -> List[str]:
        """Return a list with the names of the user (user(s) in case of a tie)
        who replies most frequently to <user>'s cheeps, or the empty list if
        there are no cheeps.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> c3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> c1.add_reply(c3)
        >>> c4 = Cheep('prof_smith', 'Prepping my lecture', \
        datetime(2019, 9 ,6))
        >>> c1.add_reply(c4)
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> chirper.post_cheep(c2)
        >>> chirper.post_cheep(c3)
        >>> chirper.post_cheep(c4)
        >>> chirper.find_fan('UofT')
        ['a_student']
        """
        userscheeps = []
        for cheep in self._cheeps:
            if cheep.user == user:
                userscheeps.append(cheep)
        if len(userscheeps) == 0:
            return []
        repliers = []
        for cheep in userscheeps:
            repliers.extend(cheep.get_repliers())
        if len(repliers) == 0:
            return []
        repliedtimes = {}
        for replier in repliers:
            if replier not in repliedtimes.keys():
                repliedtimes[replier] = 1
            else:
                repliedtimes[replier] = repliedtimes[replier] + 1
        repliedtimeslist = list(repliedtimes.items())
        sortedrepliedtimeslist = repliedtimeslist.copy()
        for i in range(len(sortedrepliedtimeslist)):
            for j in range(0, (len(sortedrepliedtimeslist) - i - 1)):
                if sortedrepliedtimeslist[j][1] >\
                        sortedrepliedtimeslist[j + 1][1]:
                    sortedrepliedtimeslist[j], sortedrepliedtimeslist[j + 1]\
                    = sortedrepliedtimeslist[j + 1], sortedrepliedtimeslist[j]
        fan = []
        for userr in sortedrepliedtimeslist:
            if userr[1] == \
                    sortedrepliedtimeslist[len(sortedrepliedtimeslist) - 1][1]:
                fan.append(userr[0])
        return fan


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'datetime', 'typing',
                                   'python_ta', 'doctest']})
