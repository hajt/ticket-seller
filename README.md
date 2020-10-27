# Ticket Seller

*Ticket Seller is a Web application for reservation and selling tickets for Events.*

## Prerequisites

- **Python** >=**3.7.9** with installed dependencies from **requirements.txt**  
- **RabbitMQ Server** >=**3.6.10**

## Local development

1. Pull this repository
2. Install the prerequisites
3. Install Python dependencies:   
`pip install -r requirements.txt`
4. Load example data:  
`python manage.py loaddata fixtures.json`  
4. Run Django server: 
`python manage.py runserver`
5. Run periodically checking and releasing expired reservations:  
`celery -A project beat -l info`  
It is possible to validate tasks execution status by running:     
`celery -A project worker -l info`

## Possible actions:

List all events:  
`GET /api/events/`  
Create event:  
`POST /api/events/`  
Retrive event detail:  
`GET /api/events/<event_id>/`  
Update event:  
`PUT /api/events/<event_id>/`  
Delete event:  
`DELETE /api/events/<event_id>/`  
Reservation statistics for event:  
`GET /api/events/<event_id>/summary/`  


List all tickets:  
`GET /api/tickets/`  
List all tickets for specific Event:  
`GET /api/tickets/?event=<event_id>`  
List only available tickets:  
`GET /api/tickets/available/`  
Create ticket:  
`POST /api/tickets/`  
Retrive ticket detail:  
`GET /api/tickets/<ticket_id>/`  
Update ticket:  
`PUT /api/tickets/<ticket_id>/`  
Delete ticket:  
`DELETE /api/tickets/<ticket_id>/`  
Reserve ticket:  
`GET /api/tickets/<ticket_id>/reserve/`  
Reservation statistics for specific Ticket:  
`GET /api/tickets/<ticket_id>/summary/`  


List all reservations:  
`GET /api/reservations/`  
List all reservations for specific Ticket:  
`GET /api/reservations/?ticket=<ticket_id>`  
Retrive reservation detail:  
`GET /api/reservations/<reservation_id>/`  
Pay reservation:  
`POST /api/reservations/<reservation_id>/pay/`  
*Needs to pass in payload: amount (required), currency and token (optional).*
