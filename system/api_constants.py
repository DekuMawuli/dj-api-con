class APIConstants:
    API_BASE_URL = "http://127.0.0.1:8000/api"
    API_VERSION = "/v1.0"
    LOGIN_URL = API_BASE_URL + API_VERSION + "/users/login/"
    CREATE_USER_URL = API_BASE_URL + API_VERSION + "/users/create/"
    RESET_PASSWORD_URL = API_BASE_URL + API_VERSION + "/users/reset_password/"
    GET_AUTH_USER_URL = API_BASE_URL + API_VERSION + "/users/me/"
    ALL_PURCHASERS_URL = API_BASE_URL + API_VERSION + "/purchaser/"
    CREATE_PURCHASER_URL = API_BASE_URL + API_VERSION + "/purchaser/"

    PURCHASER_SALES_URL = API_BASE_URL + API_VERSION + "/purchaser/{id}/sales/"
    EQUIPMENTS_URL = API_BASE_URL + API_VERSION + "/equipments/"
    CREATE_EQUIPMENTS_URL = API_BASE_URL + API_VERSION + "/equipments/"
    UPDATE_EQUIPMENTS_URL = API_BASE_URL + API_VERSION + "/equipments/"

    ALL_INSPECTIONS_URL = API_BASE_URL + API_VERSION + "/inspections/"
    CREATE_INSPECTIONS_URL = API_BASE_URL + API_VERSION + "/inspections/"
    ALL_ODOMETERS_URL = API_BASE_URL + API_VERSION + "/equipments/{id}/odometer/"
    ALL_SALES_URL = API_BASE_URL + API_VERSION + "/sales/"
    CREATE_SALES_URL = API_BASE_URL + API_VERSION + "/sales/"
    SET_TOTAL_PAID_URL = API_BASE_URL + API_VERSION + "/sales/{id}/set_paid/"
    ALL_SERVICES_URL = API_BASE_URL + API_VERSION + "/services/"
    CREATE_SERVICES_URL = API_BASE_URL + API_VERSION + "/services/"

    ALL_REFERRERS_URL = API_BASE_URL + API_VERSION + "/referrer/"
    CREATE_REFERRERS_URL = API_BASE_URL + API_VERSION + "/api/v1/referrer"

    REFERRER_SALES = API_BASE_URL + API_VERSION + "/referrer/{id}/sales/"
    ALL_SERVICE_TYPES = API_BASE_URL + API_VERSION + "/service-types/"
    CREATE_SERVICE_TYPES = API_BASE_URL + API_VERSION + "/service-types/"

    ALL_ODOMETERS = API_BASE_URL + API_VERSION + "/odomoters/"
    CREATE_ODOMETERS = API_BASE_URL + API_VERSION + "/odomoters/"
