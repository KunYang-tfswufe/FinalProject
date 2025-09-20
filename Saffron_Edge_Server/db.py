import os
import sqlite3
import threading
from datetime import datetime

_DB_PATH = os.path.join(os.path.dirname(__file__), 'data.sqlite3')
_db_lock = threading.Lock()
_conn = None


def _connect():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute('PRAGMA journal_mode=WAL;')
        _conn.execute('PRAGMA synchronous=NORMAL;')
    return _conn


def create_tables():
    conn = _connect()
    with _db_lock:
        # users
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        # roles
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
            """
        )
        # user_roles (many-to-many)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_roles (
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, role_id),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(role_id) REFERENCES roles(id) ON DELETE CASCADE
            );
            """
        )
        # devices
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                last_seen TEXT
            );
            """
        )
        # sensor_data
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                temperature REAL,
                humidity REAL,
                lux REAL,
                soil REAL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(device_id) REFERENCES devices(id) ON DELETE CASCADE
            );
            """
        )
        # control_logs
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS control_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                actuator TEXT,
                action TEXT,
                raw_command TEXT,
                success INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY(device_id) REFERENCES devices(id) ON DELETE CASCADE
            );
            """
        )
        # irrigation_policies (optional business table to reach >=6)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS irrigation_policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 0,
                soil_threshold_min REAL,
                watering_seconds INTEGER,
                updated_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY(device_id) REFERENCES devices(id) ON DELETE CASCADE
            );
            """
        )
        conn.commit()


def ensure_default_device(name: str = 'stm32_device_1') -> int:
    conn = _connect()
    with _db_lock:
        cur = conn.execute('SELECT id FROM devices WHERE name=?', (name,))
        row = cur.fetchone()
        if row:
            return row['id']
        conn.execute('INSERT INTO devices(name, description, last_seen) VALUES(?, ?, ?)',
                     (name, 'Default STM32 device', datetime.utcnow().isoformat(sep=' ', timespec='seconds')))
        conn.commit()
        return conn.execute('SELECT id FROM devices WHERE name=?', (name,)).fetchone()['id']


def update_device_last_seen(device_id: int):
    conn = _connect()
    with _db_lock:
        conn.execute('UPDATE devices SET last_seen=? WHERE id=?',
                     (datetime.utcnow().isoformat(sep=' ', timespec='seconds'), device_id))
        conn.commit()


def insert_sensor_data(device_id: int, temperature, humidity, lux, soil, ts: str):
    conn = _connect()
    with _db_lock:
        conn.execute(
            'INSERT INTO sensor_data(device_id, temperature, humidity, lux, soil, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
            (device_id, temperature, humidity, lux, soil, ts)
        )
        conn.commit()


def insert_control_log(device_id: int, actuator: str | None, action: str | None, raw_command: str, success: bool):
    conn = _connect()
    with _db_lock:
        conn.execute(
            'INSERT INTO control_logs(device_id, actuator, action, raw_command, success) VALUES (?, ?, ?, ?, ?)',
            (device_id, actuator, action, raw_command, 1 if success else 0)
        )
        conn.commit()

