from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja
app.config['SECRET_KEY'] = 'zaliczenie123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza_teatr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model bazy danych
class Rezerwacja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(100), nullable=False)
    spektakl = db.Column(db.String(100), nullable=False)
    miejsce = db.Column(db.Integer, nullable=False)

# Tworzenie tabeli
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def strona_glowna():
    if request.method == 'POST':
        # Klucz naprawy
        form_imie = request.form.get('imie')
        form_spektakl = request.form.get('spektakl')
        form_miejsce = request.form.get('miejsce')

        # Debugowanie
        print(f"Otrzymano dane: Imie={form_imie}, Spektakl={form_spektakl}, Miejsce={form_miejsce}")

        # Walidacja danych zeby nie były puste 
        
        if not form_imie or not form_spektakl or not form_miejsce:
             flash('Wypełnij wszystkie pola!', 'danger')
             return redirect(url_for('strona_glowna'))

        # Sprawdzenie miejsc
        zajete = Rezerwacja.query.filter_by(spektakl=form_spektakl, miejsce=form_miejsce).first()
        
        if zajete:
            flash(f'Miejsce {form_miejsce} na "{form_spektakl}" jest już zajęte!', 'danger')
        else:
            # Zapis do bazy
            nowy_bilet = Rezerwacja(imie=form_imie, spektakl=form_spektakl, miejsce=form_miejsce)
            db.session.add(nowy_bilet)
            db.session.commit()
            flash('Rezerwacja przyjęta pomyślnie!', 'success')
            return redirect(url_for('strona_glowna'))

    wszystkie_rezerwacje = Rezerwacja.query.all()
    return render_template('index.html', rezerwacje=wszystkie_rezerwacje)

@app.route('/usun/<int:id>')
def usun_rezerwacje(id):
    bilet = Rezerwacja.query.get_or_404(id)
    db.session.delete(bilet)
    db.session.commit()
    flash('Rezerwacja anulowana.', 'info')
    return redirect(url_for('strona_glowna'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)