import json
import instructor
from openai import OpenAI
from typing import Union
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Resource(BaseModel):
    id: str
    name: str
    type: str  # e.g., "venue", "caterer", "AV equipment"
    availability: bool
    cost_per_hour: Optional[float]

class Task(BaseModel):
    id: str
    name: str
    description: Optional[str]
    assigned_resource_ids: List[str]  # References to Resource IDs
    deadline: datetime

class Event(BaseModel):
    id: str
    name: str
    start_date: datetime
    end_date: datetime
    tasks: List[Task]

class Scheduler(BaseModel):
    events: List[Event]

def get_event_information(input_data: str) -> Union[Resource, Task, Event, Scheduler]:
    # Call the AI to parse the input data and return it in the structured form of models
    client = instructor.patch(OpenAI())
    return client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_model=Scheduler,
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": "You are an AI that helps with event planning. Understand natural language and provide structured data output.",
            },
            {
                "role": "user",
                "content": input_data,
            },
        ],
        max_tokens=500,
    )
    
    

def main():
    # Example conversational inputs
    user_input = [
        "We have a new event called 'Tech Conference 2023' starting on May 10th, ending on May 12th.",
        "We need to add a task to 'Tech Conference 2023' for setting up the main stage, which uses resource ID 'venue-123' and needs to be done by May 9th, 5 PM.",
        "What's the schedule looking like for the next month?"
    ]
    
    # Process each user input and provide a structured response
    for input_str in user_input:
        structured_data = get_event_information(input_str)
        print(structured_data)

if __name__ == "__main__":
    main()