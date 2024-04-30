class APIConstants:
    API_BASE_URL = "http://127.0.0.1:8000/api/v1.0"
    # API_BASE_URL = "http://em-api-env.eba-6fm3guem.eu-west-1.elasticbeanstalk.com/api/v1.0"
    LOGIN_URL = API_BASE_URL + "/users/login/"
    CREATE_USER_URL = API_BASE_URL + "/users/create/"
    RESET_PASSWORD_URL = API_BASE_URL + "/users/reset_password/"
    GET_AUTH_USER_URL = API_BASE_URL + "/users/me/"
    UPDATE_USER_URL = API_BASE_URL + "/users/me/"
    ALL_PURCHASERS_URL = API_BASE_URL + "/purchaser/"
    CREATE_PURCHASER_URL = API_BASE_URL + "/purchaser/"
    ALL_USERS_URL = API_BASE_URL + "/users/"

    EQUIPMENTS_URL = API_BASE_URL + "/equipments/"
    CREATE_EQUIPMENTS_URL = API_BASE_URL + "/equipments/"
    UPDATE_EQUIPMENTS_URL = API_BASE_URL + "/equipments/"

    ALL_INSPECTIONS_URL = API_BASE_URL + "/inspections/"
    CREATE_INSPECTIONS_URL = API_BASE_URL + "/inspections/"
    ALL_SALES_URL = API_BASE_URL + "/sales/"
    CREATE_SALES_URL = API_BASE_URL + "/sales/"
    SET_TOTAL_PAID_URL = API_BASE_URL + "/sales/{id}/set_paid/"
    ALL_SERVICES_URL = API_BASE_URL + "/services/"
    CREATE_SERVICES_URL = API_BASE_URL + "/services/"

    ALL_REFERRERS_URL = API_BASE_URL + "/referrer/"
    CREATE_REFERRERS_URL = API_BASE_URL + "/referrer/"

    REFERRER_SALES = API_BASE_URL + "/referrer/{id}/sales/"
    ALL_SERVICE_TYPES = API_BASE_URL + "/service-types/"
    CREATE_SERVICE_TYPES = API_BASE_URL + "/service-types/"

    ALL_ODOMETERS = API_BASE_URL + "/odomoters/"
    CREATE_ODOMETERS = API_BASE_URL + "/odomoters/"
