import flask
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

def enviar_mensagem_texto(phone_number, texto):