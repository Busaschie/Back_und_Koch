# Todolist
## Version 02

* 1 User hat N Todos
* User mit Passwordverschlüsselung

## Aufgabe
* Todo-App soll mit Passwortverschlüsseleung funktionieren
* UserRepository: create(User) modifizieren, dass User mit verschlüsseltem Passwort 
  gespeichert werden (util.py-> hash_password(...))
* implementiere : crud.py: find_user_by_credentials  ( util.py-> verify_password(...)
* Teste die Methode/Methoden in der main
