if(${IDF_TARGET} STREQUAL "linux")
    set(requires esp_stubs)
endif()

set(tcp_client_ip tcp_client.c)

idf_component_register(SRCS "tcp_client_main.c" "${tcp_client_ip}"
                                INCLUDE_DIRS "."
                                REQUIRES ${requires})
