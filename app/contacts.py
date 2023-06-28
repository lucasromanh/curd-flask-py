from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

contacts = Blueprint('usuarios', __name__, template_folder='app/templates')


@contacts.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', usuarios=data)


@contacts.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        telefono = request.form['telefono']
        email = request.form['email']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre_completo, telefono, email) VALUES (%s,%s,%s)", (nombre_completo, telefono, email))
            mysql.connection.commit()
            flash('Usuario Agregado de forma Correcta')
            return redirect(url_for('usuarios.Index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('usuarios.Index'))


@contacts.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', usuarios=data[0])


@contacts.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios
            SET nombre_completo = %s,
                email = %s,
                telefono = %s
            WHERE id = %s
        """, (nombre_completo, email, telefono, id))
        flash('Usuario Actualizado de forma Correcta')
        mysql.connection.commit()
        return redirect(url_for('usuarios.Index'))


@contacts.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario Eliminiado')
    return redirect(url_for('usuarios.Index'))
