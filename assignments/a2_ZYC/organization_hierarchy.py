"""Assignment 2: Organization Hierarchy
You must NOT use list.sort() or sorted() in your code.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Sophia Huynh
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO

# TODO: === TASK 1 ===
# Complete the merge() function and the Employee and Organization classes
# according to their docstrings.
# Go through client_code.py to find additional methods that you must
# implement.
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.

# You must NOT use list.sort() or sorted() in your code.
# Write and make use of the merge() function instead.


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    cur1 = 0
    cur2 = 0
    lst_ret = []
    while cur1 < len(lst1) or cur2 < len(lst2):
        if cur1 == len(lst1):
            lst_ret.append(lst2[cur2])
            cur2 += 1
        elif cur2 == len(lst2):
            lst_ret.append(lst1[cur1])
            cur1 += 1
        elif lst1[cur1] < lst2[cur2]:
            lst_ret.append(lst1[cur1])
            cur1 += 1
        else:
            lst_ret.append(lst2[cur2])
            cur2 += 1
    return lst_ret


class Employee:
    """An Employee: an employee in an organization.

    === Public Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.

    === Private Attributes ===
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - eid > 0
    - Within an organization, each eid only appears once. Two Employees cannot
      share the same eid.
    - salary > 0
    - 0 <= rating <= 100
    """
    eid: int
    name: str
    position: str
    salary: float
    rating: int
    _superior: Optional[Employee]
    _subordinates: List[Employee]

    # === TASK 1 ===
    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        """
        self.eid = eid
        self.name = name
        self.position = position
        self.salary = salary
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        less than <other>'s eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1 < e2
        True
        """
        return self.eid < other.eid

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        # Can this return directly
        subordinates_lst = []
        for subordinates in self._subordinates:
            subordinates_lst = merge(subordinates_lst, [subordinates])
        return subordinates_lst

    def get_all_subordinates(self) -> List[Employee]:
        """Return a list of all of the subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_all_subordinates()[0].name
        'Emma Ployee'
        >>> e3.get_all_subordinates()[1].name
        'Sue Perior'
        """
        subordinates_lst = []
        for subordinate in self._subordinates:
            subordinates_lst = merge(subordinates_lst, [subordinate])
        for subordinate in self._subordinates:
            temp_lst = subordinate.get_all_subordinates()
            subordinates_lst = merge(subordinates_lst, temp_lst)
        return subordinates_lst

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_organization_head().name
        'Bigg Boss'
        """
        if self._superior is None:
            return self
        return self._superior.get_organization_head()

    def get_superior(self) -> Optional[Employee]:
        """Returns the superior of this Employee or None if no superior exists.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_superior() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().name
        'Sue Perior'
        """
        return self._superior

    # Task 1: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def become_subordinate(self, superior: Union[Employee, None]) -> None:
        """Set this Employee's superior to <superior> and becomes a direct
        subordinate of <superior>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().eid
        2
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.become_subordinate(None)
        >>> e1.get_superior() is None
        True
        >>> e2.get_direct_subordinates()
        []
        """
        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
        self._superior = superior
        if self._superior is not None:
            superior.add_subordinate(self)

    def remove_subordinate_id(self, eid: int) -> None:
        """Remove the subordinate with the eid <eid> from this Employee's list
        of direct subordinates.

        Does NOT change the employee with eid <eid>'s superior.

        Pre-condition: This Employee has a subordinate with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e2.remove_subordinate_id(1)
        >>> e2.get_direct_subordinates()
        []
        >>> e1.get_superior() is e2
        True
        """
        subordinate_id = -1
        for i in range(len(self._subordinates)):
            if self._subordinates[i].eid == eid:
                subordinate_id = i
        if subordinate_id != -1:
            self._subordinates.pop(subordinate_id)

    def add_subordinate(self, subordinate: Employee) -> None:
        """Add <subordinate> to this Employee's list of direct subordinates.

        Does NOT change subordinate's superior.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e2.add_subordinate(e1)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.get_superior() is None
        True
        """
        subordinate_lst = [subordinate]
        self._subordinates = merge(self._subordinates, subordinate_lst)

    def get_employee(self, eid: int) -> Optional[Employee]:
        """Returns the employee with ID <eid> or None if no such employee exists
        as a subordinate of this employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_employee(1) is e1
        True
        >>> e1.get_employee(1) is e1
        True
        >>> e2.get_employee(3) is None
        True
        """
        if self.eid == eid:
            return self
        for subordinate in self._subordinates:
            subordinate_ans = subordinate.get_employee(eid)
            if subordinate_ans is not None:
                return subordinate_ans
        return None

    def get_employees_paid_more_than(self, amount: float) -> List[Employee]:
        """Get all subordinates of this employee that have a salary higher than
        <amount> (including this employee, if this employee's salary is higher
        than <amount>).

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        """
        subordinates_lst = self.get_all_subordinates()
        subordinates_ans = []
        for subordinate in subordinates_lst:
            if subordinate.salary > amount:
                subordinates_ans = merge(subordinates_ans, [subordinate])
        if self.salary > amount:
            subordinates_ans = merge(subordinates_ans, [self])
        # for subordinate in self._subordinates:
        #     temp_lst = subordinate.get_employees_paid_more_than(amount)
        #     subordinates_lst = merge(subordinates_lst, temp_lst)
        return subordinates_ans

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1. Write their headers and bodies below.

    def get_higher_paid_employees(self) -> List[Employee]:
        '''

        :return:
        '''
        head = self.get_organization_head()
        return head.get_employees_paid_more_than(self.salary)

    def get_closest_common_superior(self, eid: int) -> Employee:
        '''

        :param eid:
        :return:
        '''
        boss = self.get_organization_head()
        if boss.eid == eid:
            return boss
        cur_lst = self._get_path_to_boss()
        other_lst = boss.get_employee(eid)._get_path_to_boss()
        # print(boss.get_employee(eid)._get_path_to_boss())
        cur_p = 0
        other_p = 0
        both_boss = None
        while cur_p < len(cur_lst) and other_p < len(other_lst):
            if cur_lst[cur_p] is other_lst[other_p]:
                both_boss = cur_lst[cur_p]
            cur_p += 1
            other_p += 1
        return both_boss

    def _get_path_to_boss(self) -> List[Employee]:
        '''

        :return:
        '''
        if self._superior is None:
            return [self]
        else:
            temp_lst = self._superior._get_path_to_boss()
            temp_lst.append(self)
            return temp_lst

    # === TASK 2 ===
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        """
        if self._superior is None:
            return ''
        else:
            return self._superior.get_department_name()

    def _get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1._get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1._get_department_name()
        'Department'
        """
        if self._superior is None:
            return ''
        return self._superior._get_department_name()

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        employee_title = self._get_department_name()
        if employee_title == '':
            return self.position
        else:
            return self.position + ', ' + employee_title

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.

    def _get_department_leader(self) -> Optional[Employee]:
        if isinstance(self, Leader):
            return self
        elif self._superior is None:
            return None
        else:
            return self._superior.get_department_leader()

    def get_department_employees(self) -> List[Employee]:
        '''

        :return:
        '''
        employee_lst = self.get_all_subordinates()
        employee_lst = merge([self], employee_lst)
        return employee_lst


    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Employee]:
        """Return the leader of this Employee's department. If this Employee is
        not in a department, return None.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_department_leader().name
        'Sue Perior'
        >>> e2.get_department_leader().name
        'Sue Perior'
        """
        if isinstance(self, Leader):
            return self
        if self._superior is not None:
            return self._superior.get_department_leader()
        return None

    def become_leader(self, department_name: str) -> Leader:
        '''

        :param department_name:
        :return:
        '''
        leader = Leader(self.eid, self.name, self.position,
                        self.salary, self.rating, department_name)
        subordinate_lst = self.get_direct_subordinates()
        for subordinate in subordinate_lst:
            # print(subordinate.name)
            subordinate.become_subordinate(leader)
        superior = self.get_superior()
        if superior is not None:
            superior.remove_subordinate_id(self.eid)
            leader.become_subordinate(superior)
        return leader

    def become_employee(self) -> Employee:
        '''

        :return:
        '''
        employee = Employee(self.eid, self.name, self.position,
                            self.salary, self.rating)
        subordinate_lst = self.get_direct_subordinates()
        for subordinate in subordinate_lst:
            # print(subordinate.name)
            subordinate.become_subordinate(employee)
        superior = self.get_superior()
        if superior is not None:
            superior.remove_subordinate_id(self.eid)
            employee.become_subordinate(superior)
        return employee

    def change_department_leader(self) -> Employee:
        '''

        :return:
        '''
        head = self.get_organization_head()
        if isinstance(self, Leader):
            return head
        leader = self._get_department_leader()
        leader_superior = leader.get_superior()
        dpt_name = self.get_department_name()
        new_employee = leader.become_employee()
        new_leader = self.become_leader(dpt_name)
        new_employee.become_subordinate(new_leader)
        new_leader.become_subordinate(leader_superior)
        if leader_superior is None:
            return new_leader
        else:
            return head


    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 3.

    # Part 4: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def get_highest_rated_subordinate(self) -> Employee:
        """Return the subordinate of this employee with the highest rating.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Sue Perior'
        >>> e1.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Emma Ployee'
        """
        h_employee = None
        for subordinate in self._subordinates:
            if h_employee is None or h_employee.rating < subordinate.rating:
                h_employee = subordinate
        return h_employee

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> new_e1 = e1.swap_up()
        >>> isinstance(new_e1, Leader)
        True
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """
        # TODO Task 4: Complete the swap_up method.
        leader_name = self._superior.name
        leader_eid = self._superior.eid
        leader_rating = self._superior.rating
        self._superior.name = self.name
        self.name = leader_name
        self._superior.eid = self.eid
        self.eid = leader_eid
        self._superior.rating = self.rating
        self.rating = leader_rating
        self.become_subordinate(self._superior)
        self._superior.become_subordinate(self._superior._superior)
        return self._superior

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 4.

    def obtain_subordinates(self, ids: List[int]) -> Employee:
        '''

        :param ids:
        :return:
        '''
        head = self.get_organization_head()
        for eid in ids:
            subordinate = head.get_employee(eid)
            temp_head = _fire(subordinate)
            if temp_head is not None:
                head = temp_head
            subordinate.become_subordinate(self)
        return head

def _fire(employee: Employee) -> Optional[Employee]:
    return_head = employee.get_organization_head()
    if employee is employee.get_organization_head():
        head = employee.get_organization_head()
        max_rating = -1
        max_subordinate = None
        for subordinate in head.get_direct_subordinates():
            if max_rating == -1 or subordinate.rating > max_rating:
                max_rating = subordinate.rating
                max_subordinate = subordinate
        if max_rating == -1:
            return None
        max_subordinate.become_subordinate(None)
        return_head = max_subordinate
        superior = max_subordinate
    else:
        superior = employee.get_superior()
        superior.remove_subordinate_id(employee.eid)
    subordinate_lst = employee.get_direct_subordinates()
    for subordinate in subordinate_lst:
        subordinate.become_subordinate(superior)
    return return_head


class Organization:
    """An Organization: an organization containing employees.

    === Private Attributes ===
    _head:
        The head of the organization.

    === Representation Invariants ===
    - _head is either an Employee (or subclass of Employee) or None (if there
      are no Employees).
    - No two Employees in an Organization have the same eid.
    """
    _head: Optional[Employee]

    # === TASK 1 ===
    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        """
        self._head = head

    def get_employee(self, eid: int) -> Optional[Employee]:
        """
        Return the employee with id <eid>. If no such employee exists, return
        None.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_employee(1) is e1
        True
        >>> o.get_employee(2) is None
        True
        """
        if self._head is None:
            return None
        return self._head.get_employee(eid)

    def add_employee(self, employee: Employee, superior_id: int = None) -> None:
        """Add <employee> to this organization as the subordinate of the
        employee with id <superior_id>.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.get_employee(1) is e1
        True
        >>> e1.get_superior() is e2
        True
        """
        if superior_id is None:
            if self._head is not None:
                self._head.become_subordinate(employee)
            self.set_head(employee)
        else:
            superior_tmp = self.get_employee(superior_id)
            employee.become_subordinate(superior_tmp)

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0.0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        """
        if position is None:
            if self._head is None:
                employee_lst = []
            else:
                employee_lst = merge([self._head],
                                     self._head.get_all_subordinates())
        else:
            employee_lst = self.get_employees_with_position(position)
        if len(employee_lst) == 0:
            return 0.0
        else:
            temp_sum = 0.0
            for employee in employee_lst:
                temp_sum += employee.salary
            return temp_sum / len(employee_lst)


    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1.

    def get_head(self) -> Employee:
        '''

        :return:
        '''
        return self._head

    def get_next_free_id(self) -> int:
        '''

        :return:
        '''
        eid = 1
        while self.get_employee(eid) is not None:
            eid += 1
        return eid

    def get_employees_with_position(self, position: str) \
            -> List[Employee]:
        '''

        :param position:
        :return:
        '''
        if self._head is None:
            return []
        employee_lst = merge([self._head], self._head.get_all_subordinates())
        new_employee_lst = []
        for employee in employee_lst:
            if employee.position == position:
                new_employee_lst.append(employee)
        return new_employee_lst

    def set_head(self, head: Employee) -> None:
        '''

        :param head:
        :return:
        '''
        self._head = head

    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3.

    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4.

    def promote_employee(self, eid: int) -> None:
        '''

        :param eid:
        :return:
        '''
        employee = self.get_employee(eid)
        while employee.get_superior() is not None and \
            employee.rating >= employee.get_superior().rating:
            employee = employee.swap_up()


    def fire_employee(self, eid: int) -> None:
        '''

        :param eid:
        :return:
        '''
        employee = self.get_employee(eid)
        return_head = _fire(employee)
        # if return_head is not None:
        self.set_head(return_head)

    def fire_lowest_rated_employee(self) -> None:
        '''

        :return:
        '''
        employees_lst = self.get_head().get_all_subordinates()
        employees_lst = merge(employees_lst, [self.get_head()])
        min_rating = -1
        min_employee = None
        for employee in employees_lst:
            if min_rating == -1 or employee.rating < min_rating:
                min_employee = employee
                min_rating = employee.rating
        self.fire_employee(min_employee.eid)

    def fire_under_rating(self, rating: int) -> None:
        '''

        :param rating:
        :return:
        '''
        employees_lst = self.get_head().get_all_subordinates()
        employees_lst = merge(employees_lst, [self.get_head()])
        r = 0
        while r < min(rating, 105):
            for employee in employees_lst:
                if employee.rating == r:
                    self.fire_employee(employee.eid)
            r += 1


# === TASK 2: Leader ===
# TODO: Complete the Leader class and its methods according to their docstrings.
#       You will also need to revisit Organization and Employee to implement
#       additional methods.
#       Go through client_code.py to find additional methods that you must
#       implement.
#
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.
#
# After the completion of Task 2, you should be able to run organization_ui.py,
# though not all of the buttons will work.


class Leader(Employee):
    """A subclass of Employee. The leader of a department in an organization.

    === Private Attributes ===
    _department_name:
        The name of the department this Leader is the head of.

    === Inherited Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - All Employee RIs are inherited.
    - Department names are unique within an organization.
    """
    _department_name: str

    # === TASK 2 ===
    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Department'
        """
        Employee.__init__(self, eid, name, position, salary, rating)
        self._department_name = department

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.
    #       There may also be Employee methods that you'll need to override.

    # === TASK 2 ===

    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        """
        return self._department_name

    def _get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1._get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1._get_department_name()
        'Department'
        """
        if self._superior is None:
            return self._department_name
        dpt_str = self._superior._get_department_name()
        if dpt_str == '':
            return self._department_name
        else:
            return self._department_name + ', ' + dpt_str


    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3. If there are no methods there, consider if you need to
    #       override any of the Task 3 Employee methods.

    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4. If there are no methods there, consider if you need to
    #       override any of the Task 4 Employee methods.


# === TASK 5 ===
# TODO: Complete the create_department_salary_tree() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

class DepartmentSalaryTree:
    """A DepartmentSalaryTree: A tree representing the salaries of departments.
    The salaries considered only consist of employees directly in a department
    and not in any of their subdepartments.

    Do not change this class.

    === Public Attributes ===
    department_name:
        The name of the department that this DepartmentSalaryTree represents.
    salary:
        The average salary of the department that this DepartmentSalaryTree
        represents.
    subdepartments:
        The subdepartments of the department that this DepartmentSalaryTree
        represents.
    """
    department_name: str
    salary: float
    subdepartments: [DepartmentSalaryTree]

    def __init__(self, department_name: str, salary: float,
                 subdepartments: List[DepartmentSalaryTree]) -> None:
        """Initialize this DepartmentSalaryTree with the department name
        <department_name>, salary <salary>, and the subdepartments
        <subdepartments>.

        >>> d = DepartmentSalaryTree('Department', 30000, [])
        >>> d.department_name
        'Department'
        """
        self.department_name = department_name
        self.salary = salary
        self.subdepartments = subdepartments[:]


def create_department_salary_tree(organization: Organization) -> \
        Optional[DepartmentSalaryTree]:
    """Return the DepartmentSalaryTree corresponding to <organization>.

    If <organization> has no departments, return None.

    Pre-condition: If there is at least one department in <organization>,
    then the head of <organization> is also a Leader.

    >>> o = Organization()
    >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    >>> o.add_employee(e2)
    >>> o.add_employee(e1, 2)
    >>> o.add_employee(e3)
    >>> dst = create_department_salary_tree(o)
    >>> dst.department_name
    'Company'
    >>> dst.salary
    50000.0
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """
    # TODO Task 5: Complete the create_department_salary_tree function.
    if isinstance(organization.get_head(), Leader):
        return _create_department_salary_tree(organization.get_head())
    else:
        return None

def _get_department_employees_only(employee: Employee) -> List[Employee]:
    employee_lst = [employee]
    for subordinate in employee.get_direct_subordinates():
        if not isinstance(subordinate, Leader):
            employee_lst = merge(employee_lst,
                                 _get_department_employees_only(subordinate))
    return employee_lst

def _get_next_leaders(employee: Employee) -> List[Employee]:
    leader_lst = []
    for subordinate in employee.get_direct_subordinates():
        if isinstance(subordinate, Leader):
            leader_lst = merge(leader_lst, [subordinate])
        else:
            leader_lst = merge(leader_lst,
                               _get_next_leaders(subordinate))
    return leader_lst

def _create_department_salary_tree(employee: Employee) -> \
        DepartmentSalaryTree:
    '''

    :param employee:
    :return:
    '''
    tree_lst = []
    leader_lst = _get_next_leaders(employee)
    for leader in leader_lst:
        tree_lst.append(_create_department_salary_tree(leader))
    salary = 0.0
    employee_lst = _get_department_employees_only(employee)
    for emp in employee_lst:
        salary += emp.salary
    big_tree = DepartmentSalaryTree(employee.get_department_name(),
                                    salary / len(employee_lst), tree_lst)
    return big_tree

# def _create_department_salary_tree(employee: Employee) -> \
#         List[DepartmentSalaryTree]:
#     '''
#
#     :param employee:
#     :return:
#     '''
#     tree_lst = []
#     for subordinate in employee.get_direct_subordinates():
#         tree_lst.extend(_create_department_salary_tree(subordinate))
#     if isinstance(employee, Leader):
#         # salary, cnt = _get_department_salary(employee, True)
#         salary = 0.0
#         employee_lst = _get_department_employees_only(employee)
#         for emp in employee_lst:
#             salary += emp.salary
#         big_tree = DepartmentSalaryTree(employee.get_department_name(),
#                                         salary / len(employee_lst), tree_lst)
#         # print(employee.get_department_name())
#         # print(salary)
#         # print(cnt)
#         return [big_tree]
#     else:
#         return tree_lst

# def _get_department_salary(employee: Employee, first_leader: bool) \
# -> Tuple(float, int):
#     if isinstance(employee, Leader) and not first_leader:
#         return (0.0, 0)
#     total_salary = employee.salary
#     total_cnt = 1
#     for subordinate in employee.get_direct_subordinates():
#         salary, cnt = _get_department_salary(subordinate, False)
#         total_salary += salary
#         total_cnt += cnt
#     return (total_salary, total_cnt)


# === TASK 6 ===
# TODO: Complete the create_organization_from_file() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """
    relation_lst = []
    for line in file:
        fobj = line.strip().split(',')
        if len(fobj) > 6:
            emp = Leader(int(fobj[0]), fobj[1], fobj[2], float(fobj[3]),
                         int(fobj[4]), fobj[6])
        else:
            emp = Employee(int(fobj[0]), fobj[1], fobj[2], float(fobj[3]),
                           int(fobj[4]))
        if fobj[5] == '':
            o = Organization(emp)
            o_emp_lst = [emp.eid]
        else:
            relation_lst.append((emp, int(fobj[5])))
    tot_cnt = len(relation_lst)
    add_cnt = 0
    # assert o._head is not None
    while add_cnt < tot_cnt:
        # print(add_cnt)
        for emp_tuple in relation_lst:
            emp, fa = emp_tuple
            # str = ''
            # for i in o_emp_lst:
            #     str = str + ' - ' + i
            # print(str)
            # print(f'{emp.eid} > {fa}')
            # print(emp.eid not in o_emp_lst and fa in o_emp_lst)
            if emp.eid not in o_emp_lst and fa in o_emp_lst:
                # print(emp.eid)
                o.add_employee(emp, fa)
                o_emp_lst.append(emp.eid)
                add_cnt += 1
    return o


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'doctest', 'typing',
                                   '__future__'],
        'max-args': 7})
