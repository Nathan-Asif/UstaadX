{Note: Take logs of all my given prompts in a md file, each prompt on a new line

this is all the agents required in this app @[Agents List.txt]

the agents now we have to build are 4 and 5, lets plan that first

(we are going to build server and agents, as flutter frontend isnt ready because the design is being worked on at the moment so meanwhile we work on that first)}

{actually each prompt should be enclosed in {} and then new line}

{Lets Plan and Build Ranking Agent (Elo System):
The main component of this agent will be, on which it will be working on is the Expected Performance formula, it will be like a chess elo system and based on this we will find the relevant technicians for the customer based on their needs and purpose

Our AI Agent (Gemini LLM) will work based on this and perform}

{Since we dont have live UI for dynamic and registered users data, we will have to use some mock data for it, for that lets integrate and connect supabase for db, and create migrations and mock data seeding files in it to use that data for our agents:
lets plan it for our first agent, we'll upgrade the db tables/documents as per other agents and other aspects of the app.

At the moment we need these tables/documents:
Customers
Technicians
Agents (so we can toggle it on/off its use, keep track of its log in AgentLog with its id)
CustomerActivity (to keep log of customers activity conversation with the agent, and when actual technician intervenes his and customers conversations) like this for example:
{
[date/time or id]:{"customer": "I need a technician to fix my AC at address", "agent": "Sure I can find a technician for you" },
[date/time or id]:{"technician": "Hello, Im glad you accepted me for the job", "customer": "Just be on time"}
}


these are for example we'll enhance them}

{provide me the queries to create all these tables schema in the supabase}

{created the UstaadX supabase db and the specific taables, now create a migration mock data setup to insert mock data into these tables}

{Lets connect our supabase db with our fastapi orchestrator first and then we will programmatically seed into the db

SUPABASE_URL=https://lxutyoztfpmoxnaunrkm.supabase.co
SUPABASE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}

{give me the command to run it again}

{I have successfully seeded the data with this:
python infra/scripts/test_ranking_agent.py

now next up setup the LLM/AI for our AI Agent to work on (gemini): xxxxxxxxxxxxxxxx}

{Now since all the foundational components are created and added, lets start building the RankingAgent}

{btw have you created the agent using the gemini agent sdk?}

{does this current agent of ours peforms an AI Agent job of like making decisions itself, performing tasks itself etc}

{ok but our rank agent doesnt act entirely based on static code, conditinos and data right it has the ability to make decisinos and determining on its own?}

{make apps/backend_api/app/core/config-example.py as a tempalate without values in it}
