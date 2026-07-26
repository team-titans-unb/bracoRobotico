add_executable(Test)

target_sources(Test
	PRIVATE
		test.cpp
)

target_link_libraries(Test
	PRIVATE
		PID
)