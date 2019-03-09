# order-status-checker
The issue:
Currently, for an average of 30 ServiceNow order tickets per worker, it takes my coworkers and myself about 90-120 minutes to update our tickets.  We have a standard of updating these tickets at least once every 48 hours so I estimate we spend 3-4 hours every week on order updates.

The goal:
To allow my coworkers and myself to quickly check the order status of our placed orders from Hewlett Packard. Currently, after login, it takes several clicks to get to HP order status page.  We then copy and paste the "HP PO#" into the search bar and what is returned is a table with two or several tabs depending on the results.  Then, after a quick analysis of the table, we type out our findings into ServiceNow where either the Neighborhood IT or customer may view our comments. 

The HP website we use is not their commercial website, but rather a portal specific to institutions and enterprise and there appears to be no API for retrieving the data.  My manager and myself reached out to numerous HP representatives that we work with routinely and reached dead ends finding an API.  Therefore, I am using Selenium to emulate human action and navigate to the order status page and retrieve the data for the given HP PO#.

Once I reach satisfaction that the tool is working as intended, the plan is to extend this to our Apple orders.
