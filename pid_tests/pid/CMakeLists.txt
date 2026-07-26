add_library(PID)

target_sources(PID
	PRIVATE
		pid.cpp
	PUBLIC
		FILE_SET HEADERS
		FILES
			pid.h
)