from typing import Callable, Dict, List, Type,Union
from src.domain import commands
from src.domain import  events
from src.domain import queries
from src.service_layer.unityofwork import MongoRedisUnitOfWork

Message = Union[commands.Command ,events.Event]


class MessageBus:
    def __init__(
        self,
        uow: MongoRedisUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],
        querie_handlers:Dict[Type[queries.Query], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.querie_handlers=querie_handlers

    def handle(self, message: Message):
        self.queue = [message]
        
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
               self.handle_event(message)
               
            elif isinstance(message, commands.Command):
                result=self.handle_command(message)
                return result
            elif isinstance(message,queries.Query):
                result=self.handle_querie(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                # Gérer les exceptions et les erreurs ici
                continue

    def handle_command(self, command: commands.Command):
        try:
            handler = self.command_handlers[type(command)]
            result =handler(command) 
            self.queue.extend(self.uow.collect_new_events())
            return result
        except Exception:
            # Gérer les exceptions et les erreurs ici
            raise
    def handle_querie(self, querie:queries.Query):
       try:
           handler=self.querie_handlers[type(querie)]
           result=handler(querie)
           self.queue.extend(self.uow.collect_new_events())
           return result
       except Exception:
           raise

           