db = db.getSiblingDB('jokes_db');
db.createUser(
    {
        user: 'admin',
        pwd:  'admin',
        roles: [{role: 'dbOwner', db: 'jokes_db'}],
    }
);