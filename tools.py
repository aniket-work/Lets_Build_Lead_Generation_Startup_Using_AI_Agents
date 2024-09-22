# tools.py
import json
import os

from langchain_core.tools import tool
from constants import (
    AVERAGE_ENERGY_SAVINGS_PERCENTAGE, THERMOSTAT_COST,
    INSTALLATION_COST, SYSTEM_LIFETIME_YEARS, INVALID_INPUT_ERROR
)

@tool
def estimate_savings(monthly_cost: float) -> dict:
    """
    Estimate the potential savings when using a Smart Thermostat based on the user's monthly electricity cost.

    Args:
        monthly_cost (float): The user's current monthly electricity cost in dollars.

    Returns:
        dict: A dictionary containing savings information or an error message.
    """
    try:
        monthly_cost = float(monthly_cost)
        if monthly_cost <= 0:
            return {"error": INVALID_INPUT_ERROR.format(monthly_cost)}

        annual_cost = monthly_cost * 12
        annual_savings = annual_cost * AVERAGE_ENERGY_SAVINGS_PERCENTAGE
        total_savings = annual_savings * SYSTEM_LIFETIME_YEARS
        total_cost = THERMOSTAT_COST + INSTALLATION_COST
        net_savings = total_savings - total_cost

        return {
            "estimated_annual_savings": round(annual_savings, 2),
            "total_cost": round(total_cost, 2),
            "net_savings_10_years": round(net_savings, 2),
            "payback_period": round(total_cost / annual_savings, 1)
        }
    except (ValueError, TypeError):
        return {"error": INVALID_INPUT_ERROR.format(monthly_cost)}


@tool
def store_contact_info(name: str, email: str, phone: str) -> dict:
    """
    Store the contact information of a potential lead in a JSON database.

    Args:
        name (str): The name of the potential customer.
        email (str): The email address of the potential customer.
        phone (str): The phone number of the potential customer.

    Returns:
        dict: A dictionary confirming the storage of contact information.
    """
    contact_info = {
        "name": name,
        "email": email,
        "phone": phone
    }

    file_path = 'leads_database.json'

    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        data.append(contact_info)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return {"message": "Contact information stored successfully."}
    except json.JSONDecodeError:
        # If the file exists but is empty or corrupted, start with an empty list
        data = [contact_info]
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return {"message": "Contact information stored successfully (reset database)."}
    except Exception as e:
        return {"error": f"An error occurred while storing contact information: {str(e)}"}
