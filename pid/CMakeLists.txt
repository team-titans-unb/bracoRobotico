add_library(PID)

add_target_sources(PID
	public
		pid.cpp
	private
		pid.h
)

add_executable(Test)

add_target_sources(Test
	public
		test.cpp
)