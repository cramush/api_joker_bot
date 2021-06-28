db = db.getSiblingDB('jokes_db');
db.createUser(
    {
        user: 'admin',
        pwd:  'admin',
        roles: [{role: 'readWrite', db: 'jokes_db'}],
    }
);