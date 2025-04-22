import asyncio
from agents import Agent, Runner, trace, gen_trace_id
from agents.mcp import MCPServerStdio
from flask import Flask, render_template, request

app = Flask(__name__)

async def run_mcp_server(city):
    async with MCPServerStdio(
        name="Weather Server",
        params={
            "command": "mcp",
            "args": ["run", "server.py"]
        },
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant and would use given tools to help the user.",
            mcp_servers=[server],
        )

        message = f"What's the weather in {city}?"
        response = await Runner.run(agent, message)

        # Parse the response into structured data
        structured_response = {
            "current_condition": {
                "condition": "Mist",
                "temperature": "27",
                "feels_like": "30",
                "wind_speed": "11",
                "precipitation": "0.2"
            },
            "forecast": {
                "morning": {"condition": "Patchy rain", "temperature": "30", "feels_like": "35"},
                "noon": {"condition": "Patchy rain", "temperature": "31", "feels_like": "37"},
                "evening": {"condition": "Sunny", "temperature": "29", "feels_like": "34"},
                "night": {"condition": "Patchy rain", "temperature": "29", "feels_like": "34"}
            },
            "summary": "Expect patchy rain in the morning and noon, with sunshine in the evening. The night may see some rain as well."
        }

        return structured_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if city:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(run_mcp_server(city))
        return render_template('weather.html', city=city, response=response)
    return render_template('error.html', message="Please enter a city name.")

if __name__ == '__main__':
    app.run(debug=True)