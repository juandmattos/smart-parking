from pickletools import pyset
import psycopg2
from datetime import datetime

conn = psycopg2.connect(database="postgres",
                        host="192.168.68.109",
                        user="pi",
                        password="apice868",
                        port="5432")


data = """{
    "parking_id": "1",
    "parking_name": "Shopping Tres Cruces",
    "parking_description": "Parking del Shopping Tres Cruces",
    "parking_address": "La Pasiva, 1825, Bulevar General Artigas, Tres Cruces, Montevideo, 11600, Uruguay",
    "parking_closed": false,
    "parking_latitude": "-34.8943081",
    "parking_longitude": "-56.1664375",
    "parking_weather_status": "Clouds",
    "parking_weather_status_detailed": "broken clouds",
    "parking_wind_speed": 8.49,
    "parking_holiday_status": false,
    "parking_holiday_description": null,
    "parking_holiday_type": "L",
    "parking_timestamp": "22/10/2022|22:19:51",
    "parking_summary": {
        "coefficients": {
            "0to20Coef": "1.1",
            "20to40Coef": "1.2",
            "40to60Coef": "1.4",
            "60to80Coef": "1.8",
            "80to100Coef": "2"
        },
        "hasDynamicPrice": true,
        "levels": [
            {
                "level_id": "1",
                "areas": [
                    {
                        "area_id": "1",
                        "area_occupation_percentage_target": "15"
                    },
                    {
                        "area_id": "2",
                        "area_occupation_percentage_target": "20"
                    },
                    {
                        "area_id": "3",
                        "area_occupation_percentage_target": "30"
                    }
                ]
            },
            {
                "level_id": "2",
                "areas": [
                    {
                        "area_id": "1",
                        "area_occupation_percentage_target": "15"
                    },
                    {
                        "area_id": "2",
                        "area_occupation_percentage_target": "20"
                    },
                    {
                        "area_id": "3",
                        "area_occupation_percentage_target": "30"
                    },
                    {
                        "area_id": "4",
                        "area_occupation_percentage_target": "60"
                    }
                ]
            },
            {
                "level_id": "3",
                "areas": [
                    {
                        "area_id": "1",
                        "area_occupation_percentage_target": "15"
                    },
                    {
                        "area_id": "2",
                        "area_occupation_percentage_target": "80"
                    }
                ]
            }
        ]
    },
    "levels": [
        {
            "level_id": "1",
            "level_name": "Piso 1",
            "level_average_price": "11.0",
            "level_occupation": "Almost Full",
            "level_occupied_spots": "17",
            "level_available_spots": "16",
            "level_total_spots": "33",
            "level_occupation_percentage": "51",
            "areas": [
                {
                    "area_id": "1",
                    "area_name": "A",
                    "area_description": "blue",
                    "area_occupation": "Almost Empty",
                    "area_occupied_spots": "2",
                    "area_total_spots": "7",
                    "area_available_spots": "5",
                    "area_occupation_percentage": "28",
                    "area_color": "#3244a8",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": true,
                            "slot_description": "1A",
                            "slot_price": "200",
                            "slot_type": "motorcycles"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": false,
                            "slot_description": "2A",
                            "slot_price": "200",
                            "slot_type": "motorcycles"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": false,
                            "slot_description": "3A",
                            "slot_price": "200",
                            "slot_type": "motorcycles"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": false,
                            "slot_description": "4A",
                            "slot_price": "200",
                            "slot_type": "motorcycles"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": false,
                            "slot_description": "5A",
                            "slot_price": "200",
                            "slot_type": "motorcycles"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": false,
                            "slot_description": "6A",
                            "slot_price": "200",
                            "slot_type": "motorcycles"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": true,
                            "slot_description": "7A",
                            "slot_price": "200",
                            "slot_type": "motorcycles"
                        }
                    ]
                },
                {
                    "area_id": "2",
                    "area_name": "B",
                    "area_description": "orange",
                    "area_occupation": "Almost Full",
                    "area_occupied_spots": "10",
                    "area_total_spots": "17",
                    "area_available_spots": "7",
                    "area_occupation_percentage": "58",
                    "area_color": "#cf852b",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": true,
                            "slot_description": "1B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": true,
                            "slot_description": "2B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": false,
                            "slot_description": "3B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": false,
                            "slot_description": "4B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": true,
                            "slot_description": "5B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": true,
                            "slot_description": "6B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": true,
                            "slot_description": "7B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "8",
                            "slot_state": true,
                            "slot_description": "8B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "9",
                            "slot_state": true,
                            "slot_description": "9B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "10",
                            "slot_state": true,
                            "slot_description": "10B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "11",
                            "slot_state": true,
                            "slot_description": "11B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "12",
                            "slot_state": false,
                            "slot_description": "12B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "13",
                            "slot_state": false,
                            "slot_description": "13B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "14",
                            "slot_state": false,
                            "slot_description": "14B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "15",
                            "slot_state": true,
                            "slot_description": "15B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "16",
                            "slot_state": false,
                            "slot_description": "16B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "17",
                            "slot_state": false,
                            "slot_description": "17B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        }
                    ]
                },
                {
                    "area_id": "3",
                    "area_name": "C",
                    "area_description": "purple",
                    "area_occupation": "Almost Full",
                    "area_occupied_spots": "5",
                    "area_total_spots": "9",
                    "area_available_spots": "4",
                    "area_occupation_percentage": "55",
                    "area_color": "#9319bf",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": false,
                            "slot_description": "1C",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": true,
                            "slot_description": "2C",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": true,
                            "slot_description": "3C",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": true,
                            "slot_description": "4C",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": true,
                            "slot_description": "5C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": false,
                            "slot_description": "6C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": false,
                            "slot_description": "7C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "8",
                            "slot_state": true,
                            "slot_description": "8C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "9",
                            "slot_state": false,
                            "slot_description": "9C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        }
                    ]
                }
            ]
        },
        {
            "level_id": "2",
            "level_name": "Piso 2",
            "level_average_price": "10.25",
            "level_occupation": "Almost Empty",
            "level_occupied_spots": "20",
            "level_available_spots": "21",
            "level_total_spots": "41",
            "level_occupation_percentage": "48",
            "areas": [
                {
                    "area_id": "1",
                    "area_name": "A",
                    "area_description": "blue",
                    "area_occupation": "Almost Full",
                    "area_occupied_spots": "7",
                    "area_total_spots": "13",
                    "area_available_spots": "6",
                    "area_occupation_percentage": "53",
                    "area_color": "#3244a8",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": true,
                            "slot_description": "1A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": false,
                            "slot_description": "2A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": true,
                            "slot_description": "3A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": true,
                            "slot_description": "4A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": false,
                            "slot_description": "5A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": false,
                            "slot_description": "6A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": false,
                            "slot_description": "7A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "8",
                            "slot_state": true,
                            "slot_description": "8A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "9",
                            "slot_state": false,
                            "slot_description": "9A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "10",
                            "slot_state": true,
                            "slot_description": "10A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "11",
                            "slot_state": true,
                            "slot_description": "11A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "12",
                            "slot_state": true,
                            "slot_description": "12A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "13",
                            "slot_state": false,
                            "slot_description": "13A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        }
                    ]
                },
                {
                    "area_id": "2",
                    "area_name": "B",
                    "area_description": "orange",
                    "area_occupation": "Almost Empty",
                    "area_occupied_spots": "7",
                    "area_total_spots": "15",
                    "area_available_spots": "8",
                    "area_occupation_percentage": "46",
                    "area_color": "#cf852b",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": false,
                            "slot_description": "1B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": true,
                            "slot_description": "2B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": true,
                            "slot_description": "3B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": false,
                            "slot_description": "4B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": true,
                            "slot_description": "5B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": false,
                            "slot_description": "6B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": false,
                            "slot_description": "7B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "8",
                            "slot_state": true,
                            "slot_description": "8B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "9",
                            "slot_state": false,
                            "slot_description": "9B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "10",
                            "slot_state": false,
                            "slot_description": "10B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "11",
                            "slot_state": true,
                            "slot_description": "11B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "12",
                            "slot_state": false,
                            "slot_description": "12B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "13",
                            "slot_state": false,
                            "slot_description": "13B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "14",
                            "slot_state": true,
                            "slot_description": "14B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "15",
                            "slot_state": true,
                            "slot_description": "15B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        }
                    ]
                },
                {
                    "area_id": "3",
                    "area_name": "C",
                    "area_description": "purple",
                    "area_occupation": "Almost Full",
                    "area_occupied_spots": "5",
                    "area_total_spots": "8",
                    "area_available_spots": "3",
                    "area_occupation_percentage": "62",
                    "area_color": "#9319bf",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": true,
                            "slot_description": "1C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": false,
                            "slot_description": "2C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": false,
                            "slot_description": "3C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": true,
                            "slot_description": "4C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": true,
                            "slot_description": "5C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": false,
                            "slot_description": "6C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": true,
                            "slot_description": "7C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "8",
                            "slot_state": true,
                            "slot_description": "8C",
                            "slot_price": "200",
                            "slot_type": "cars"
                        }
                    ]
                },
                {
                    "area_id": "4",
                    "area_name": "D",
                    "area_description": "Light Brown",
                    "area_occupation": "Empty",
                    "area_occupied_spots": "1",
                    "area_total_spots": "5",
                    "area_available_spots": "4",
                    "area_occupation_percentage": "20",
                    "area_color": "#a67a5b",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": false,
                            "slot_description": "1D",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": false,
                            "slot_description": "2D",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": false,
                            "slot_description": "3D",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": false,
                            "slot_description": "4D",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": true,
                            "slot_description": "5D",
                            "slot_price": "200",
                            "slot_type": "cars"
                        }
                    ]
                }
            ]
        },
        {
            "level_id": "3",
            "level_name": "Piso 3",
            "level_average_price": "11.0",
            "level_occupation": "Almost Full",
            "level_occupied_spots": "15",
            "level_available_spots": "7",
            "level_total_spots": "22",
            "level_occupation_percentage": "68",
            "areas": [
                {
                    "area_id": "1",
                    "area_name": "A",
                    "area_description": "blue",
                    "area_occupation": "Almost Full",
                    "area_occupied_spots": "6",
                    "area_total_spots": "10",
                    "area_available_spots": "4",
                    "area_occupation_percentage": "60",
                    "area_color": "#3244a8",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": false,
                            "slot_description": "1A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": true,
                            "slot_description": "2A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": true,
                            "slot_description": "3A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": true,
                            "slot_description": "4A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": true,
                            "slot_description": "5A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": false,
                            "slot_description": "6A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": true,
                            "slot_description": "7A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "8",
                            "slot_state": false,
                            "slot_description": "8A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "9",
                            "slot_state": false,
                            "slot_description": "9A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        },
                        {
                            "slot_id": "10",
                            "slot_state": true,
                            "slot_description": "10A",
                            "slot_price": "200",
                            "slot_type": "cars"
                        }
                    ]
                },
                {
                    "area_id": "2",
                    "area_name": "B",
                    "area_description": "orange",
                    "area_occupation": "Almost Full",
                    "area_occupied_spots": "9",
                    "area_total_spots": "12",
                    "area_available_spots": "3",
                    "area_occupation_percentage": "75",
                    "area_color": "#cf852b",
                    "area_summary": {
                        "hasFreeHours": true,
                        "freeHourUntil": "2",
                        "hourFee": "80",
                        "dayFee": "300",
                        "monthFee": "2000"
                    },
                    "area_average_price": "200",
                    "slots": [
                        {
                            "slot_id": "1",
                            "slot_state": false,
                            "slot_description": "1B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "2",
                            "slot_state": true,
                            "slot_description": "2B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "3",
                            "slot_state": false,
                            "slot_description": "3B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "4",
                            "slot_state": true,
                            "slot_description": "4B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "5",
                            "slot_state": true,
                            "slot_description": "5B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "6",
                            "slot_state": true,
                            "slot_description": "6B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "7",
                            "slot_state": true,
                            "slot_description": "7B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "8",
                            "slot_state": false,
                            "slot_description": "8B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "9",
                            "slot_state": true,
                            "slot_description": "9B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "10",
                            "slot_state": true,
                            "slot_description": "10B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "11",
                            "slot_state": true,
                            "slot_description": "11B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        },
                        {
                            "slot_id": "12",
                            "slot_state": true,
                            "slot_description": "12B",
                            "slot_price": "200",
                            "slot_type": "trucks"
                        }
                    ]
                }
            ]
        }
    ]
}"""


cursor = conn.cursor()

sql_update = "UPDATE public.parkingsdata SET data = %s, audit_time = %s WHERE parking_name = %s"
#sql_update = "UPDATE public.parkingsdata SET audit_time = NOW() where id = %s"

cursor.execute(sql_update, (data, datetime.now().strftime('%Y-%m-%d %T'), 'TresCrucesShopping'))
#cursor.execute(sql_update, ("1"))

updated_rows = cursor.rowcount
print(updated_rows)
# Commit the changes to the database
conn.commit()

#cursor.execute("UPDATE public.parkingsdata SET audit_time = NOW() WHERE parking_name = 'TresCrucesShopping'")

#print(cursor.fetchone())