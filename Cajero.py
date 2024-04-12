
import tkinter as tk
from tkinter import messagebox
import sqlite3
import getpass

# Conexión a la base de datos SQLite
conn = sqlite3.connect('cajero.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    contraseña TEXT,
    saldo REAL
)
''')

# Crear tabla para el historial de transacciones si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    tipo TEXT,
    cantidad REAL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
)
''')

conn.commit()

# Diccionario para manejar los textos en diferentes idiomas
texts = {
    'es': {
        'welcome_message': '¡Bienvenidos al Cajero Automático CashEBAS!',
        'create_account': 'Crear cuenta',
        'login': 'Iniciar sesión',
        'account_created': 'Cuenta creada exitosamente.',
        'user_exists_error': 'El nombre de usuario ya está en uso.',
        'login_error': 'Credenciales incorrectas.',
        'current_balance': 'Saldo actual: ',
        'destination_account': 'Cuenta destino:',
        'transfer_amount': 'Cantidad a transferir:',
        'withdraw_amount': 'Cantidad a retirar:',
        'insufficient_funds_error': 'Saldo insuficiente.',
        'destination_not_found_error': 'La cuenta destino no existe.',
        'transfer_success': 'Transferencia exitosa de {amount} a {destination}.',
        'withdraw_success': 'Retiro exitoso de {amount}.',
        'transaction_history': 'Historial de transacciones',
        'transaction_id': 'ID:',
        'transaction_type': 'Tipo:',
        'transaction_amount': 'Cantidad:',
        'transaction_date': 'Fecha:',
        'username': 'Nombre de usuario:',
        'password': 'Contraseña:',
        'perform_operations': 'Realizar Operaciones'
    },
    'en': {
        'welcome_message': 'Welcome to CashEBAS ATM!',
        'create_account': 'Create Account',
        'login': 'Log In',
        'account_created': 'Account created successfully.',
        'user_exists_error': 'Username already in use.',
        'login_error': 'Incorrect credentials.',
        'current_balance': 'Current balance: ',
        'destination_account': 'Destination account:',
        'transfer_amount': 'Amount to transfer:',
        'withdraw_amount': 'Amount to withdraw:',
        'insufficient_funds_error': 'Insufficient funds.',
        'destination_not_found_error': 'Destination account not found.',
        'transfer_success': 'Transfer successful from {amount} to {destination}.',
        'withdraw_success': 'Withdrawal successful of {amount}.',
        'transaction_history': 'Transaction History',
        'transaction_id': 'ID:',
        'transaction_type': 'Type:',
        'transaction_amount': 'Amount:',
        'transaction_date': 'Date:',
        'username': 'Username:',
        'password': 'Password:',
        'perform_operations': 'Perform Operations'
    }
}

# Idioma predeterminado
current_language = 'es'

def switch_language(lang):
    global current_language
    current_language = lang

def get_text(key):
    return texts[current_language][key]

def crear_cuenta():
    ventana_crear_cuenta = tk.Toplevel(root)
    ventana_crear_cuenta.title(get_text('create_account'))

    lbl_nombre = tk.Label(ventana_crear_cuenta, text=get_text('username'))
    lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_crear_cuenta)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    lbl_contraseña = tk.Label(ventana_crear_cuenta, text=get_text('password'))
    lbl_contraseña.grid(row=1, column=0, padx=10, pady=10)
    entry_contraseña = tk.Entry(ventana_crear_cuenta, show="*")
    entry_contraseña.grid(row=1, column=1, padx=10, pady=10)

    def guardar_cuenta():
        nombre = entry_nombre.get()
        contraseña = entry_contraseña.get()

        try:
            cursor.execute('INSERT INTO usuarios (nombre, contraseña, saldo) VALUES (?, ?, ?)', (nombre, contraseña, 0))
            conn.commit()
            messagebox.showinfo("Éxito", get_text('account_created'))
            ventana_crear_cuenta.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", get_text('user_exists_error'))

    btn_guardar = tk.Button(ventana_crear_cuenta, text=get_text('save'), command=guardar_cuenta)
    btn_guardar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def iniciar_sesion():
    ventana_inicio_sesion = tk.Toplevel(root)
    ventana_inicio_sesion.title(get_text('login'))

    lbl_nombre = tk.Label(ventana_inicio_sesion, text=get_text('username'))
    lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_inicio_sesion)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    lbl_contraseña = tk.Label(ventana_inicio_sesion, text=get_text('password'))
    lbl_contraseña.grid(row=1, column=0, padx=10, pady=10)
    entry_contraseña = tk.Entry(ventana_inicio_sesion, show="*")
    entry_contraseña.grid(row=1, column=1, padx=10, pady=10)

    def verificar_credenciales():
        nombre = entry_nombre.get()
        contraseña = entry_contraseña.get()

        cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?', (nombre, contraseña))
        usuario = cursor.fetchone()

        if usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario[1]}")
            ventana_inicio_sesion.destroy()
            mostrar_operaciones(usuario)
        else:
            messagebox.showerror("Error", get_text('login_error'))

    btn_iniciar_sesion = tk.Button(ventana_inicio_sesion, text=get_text('login'), command=verificar_credenciales)
    btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def mostrar_operaciones(usuario):
    ventana_operaciones = tk.Toplevel(root)
    ventana_operaciones.title("Operaciones en el cajero")

    lbl_saldo = tk.Label(ventana_operaciones, text=f"{get_text('current_balance')} {usuario[3]:.2f}")
    lbl_saldo.pack(padx=10, pady=5)

    lbl_destino = tk.Label(ventana_operaciones, text=get_text('destination_account'))
    lbl_destino.pack(padx=10, pady=5)
    entry_destino = tk.Entry(ventana_operaciones)
    entry_destino.pack(padx=10, pady=5)

    lbl_cantidad_transferir = tk.Label(ventana_operaciones, text=get_text('transfer_amount'))
    lbl_cantidad_transferir.pack(padx=10, pady=5)
    entry_cantidad_transferir = tk.Entry(ventana_operaciones)
    entry_cantidad_transferir.pack(padx=10, pady=5)

    lbl_cantidad_retirar = tk.Label(ventana_operaciones, text=get_text('withdraw_amount'))
    lbl_cantidad_retirar.pack(padx=10, pady=5)
    entry_cantidad_retirar = tk.Entry(ventana_operaciones)
    entry_cantidad_retirar.pack(padx=10, pady=5)

    def realizar_operaciones():
        destino = entry_destino.get()
        cantidad_transferir = float(entry_cantidad_transferir.get())
        cantidad_retirar = float(entry_cantidad_retirar.get())

        if cantidad_transferir > 0:
            cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (destino,))
            usuario_destino = cursor.fetchone()

            if usuario_destino:
                if usuario[3] >= cantidad_transferir:
                    nuevo_saldo_origen = usuario[3] - cantidad_transferir
                    nuevo_saldo_destino = usuario_destino[3] + cantidad_transferir

                    cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (nuevo_saldo_origen, usuario[0]))
                    cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (nuevo_saldo_destino, usuario_destino[0]))
                    cursor.execute('INSERT INTO transacciones (usuario_id, tipo, cantidad) VALUES (?, ?, ?)', (usuario[0], 'Transferencia salida', cantidad_transferir))
                    cursor.execute('INSERT INTO transacciones (usuario_id, tipo, cantidad) VALUES (?, ?, ?)', (usuario_destino[0], 'Transferencia entrada', cantidad_transferir))
                    conn.commit()

                    messagebox.showinfo("Éxito", get_text('transfer_success').format(amount=cantidad_transferir, destination=destino))
                    lbl_saldo.config(text=f"{get_text('current_balance')} {nuevo_saldo_origen}")
                else:
                    messagebox.showerror("Error", get_text('insufficient_funds_error'))
            else:
                messagebox.showerror("Error", get_text('destination_not_found_error'))

        if cantidad_retirar > 0:
            if usuario[3] >= cantidad_retirar:
                nuevo_saldo = usuario[3] - cantidad_retirar
                cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (nuevo_saldo, usuario[0]))
                cursor.execute('INSERT INTO transacciones (usuario_id, tipo, cantidad) VALUES (?, ?, ?)', (usuario[0], 'Retiro', cantidad_retirar))
                conn.commit()

                messagebox.showinfo("Éxito", get_text('withdraw_success').format(amount=cantidad_retirar))
                lbl_saldo.config(text=f"{get_text('current_balance')} {nuevo_saldo}")
            else:
                messagebox.showerror("Error", get_text('insufficient_funds_error'))

    def ver_historial_usuario():
        ver_historial(usuario)

    btn_realizar_operaciones = tk.Button(ventana_operaciones, text=get_text('perform_operations'), command=realizar_operaciones)
    btn_realizar_operaciones.pack(padx=10, pady=10)

    btn_ver_historial = tk.Button(ventana_operaciones, text=get_text('transaction_history'), command=ver_historial_usuario)
    btn_ver_historial.pack(padx=10, pady=10)

def ver_historial(usuario):
    ventana_historial = tk.Toplevel(root)
    ventana_historial.title(get_text('transaction_history'))

    lbl_titulo = tk.Label(ventana_historial, text=get_text('transaction_history'), font=("Arial", 12, "bold"))
    lbl_titulo.pack(padx=10, pady=10)

    scrollbar = tk.Scrollbar(ventana_historial)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    historial_text = tk.Text(ventana_historial, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    historial_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    scrollbar.config(command=historial_text.yview)

    cursor.execute('SELECT * FROM transacciones WHERE usuario_id = ?', (usuario[0],))
    transacciones = cursor.fetchall()

    for transaccion in transacciones:
        historial_text.insert(tk.END, f"{get_text('transaction_id')}: {transaccion[0]}\n")
        historial_text.insert(tk.END, f"{get_text('transaction_type')}: {transaccion[2]}\n")
        historial_text.insert(tk.END, f"{get_text('transaction_amount')}: {transaccion[3]}\n")
        historial_text.insert(tk.END, f"{get_text('transaction_date')}: {transaccion[4]}\n\n")

    historial_text.config(state=tk.DISABLED)

def main():
    global root
    root = tk.Tk()
    root.title("Cajero Automático CashEBAS")

    lbl_bienvenida = tk.Label(root, text=get_text('welcome_message'), bg="#F0F0F0", fg="#333333", font=("Arial", 14, "bold"))
    lbl_bienvenida.pack(padx=10, pady=10)

    btn_crear_cuenta = tk.Button(root, text=get_text('create_account'), command=crear_cuenta, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_crear_cuenta.pack(padx=10, pady=5)

    btn_iniciar_sesion = tk.Button(root, text=get_text('login'), command=iniciar_sesion, bg="#008CBA", fg="white", font=("Arial", 10, "bold"))
    btn_iniciar_sesion.pack(padx=10, pady=5)

    # Botones para cambiar idioma
    def switch_to_spanish():
        switch_language('es')
        refresh_texts()
    def switch_to_english():
        switch_language('en')
        refresh_texts()

    btn_spanish = tk.Button(root, text="Español", command=switch_to_spanish)
    btn_spanish.pack(side=tk.LEFT, padx=10, pady=5)
    btn_english = tk.Button(root, text="English", command=switch_to_english)
    btn_english.pack(side=tk.LEFT, padx=10, pady=5)

    root.mainloop()

def refresh_texts():
    global lbl_bienvenida, btn_crear_cuenta, btn_iniciar_sesion

    lbl_bienvenida.config(text=get_text('welcome_message'))
    btn_crear_cuenta.config(text=get_text('create_account'))
    btn_iniciar_sesion.config(text=get_text('login'))

if __name__ == "__main__":
    main()
