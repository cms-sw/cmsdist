if(NOT TARGET Dyninst::Dyninst)
    add_library(Dyninst::Dyninst INTERFACE IMPORTED)
    message(STATUS "Adding additional target Dyninst::Dyninst")
    target_link_libraries(Dyninst::Dyninst
        INTERFACE
            Dyninst::dyninstAPI
            Dyninst::parseAPI
            Dyninst::instructionAPI
            Dyninst::symtabAPI)
endif()
