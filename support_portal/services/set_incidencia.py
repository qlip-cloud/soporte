import frappe

def handler(task, method):
    task.issue = task.subject
