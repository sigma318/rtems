rtems_tests_PROGRAMS = smpipi01
smpipi01_SOURCES = init.c

dist_rtems_tests_DATA = smpipi01.scn smpipi01.doc

include $(RTEMS_ROOT)/make/custom/@RTEMS_BSP@.cfg
include $(top_srcdir)/../automake/compile.am
include $(top_srcdir)/../automake/leaf.am

AM_CPPFLAGS += -I$(top_srcdir)/../support/include

LINK_OBJS = $(smpipi01_OBJECTS)
LINK_LIBS = $(smpipi01_LDLIBS)

smpipi01$(EXEEXT): $(smpipi01_OBJECTS) $(smpipi01_DEPENDENCIES)
	@rm -f smpipi01$(EXEEXT)
	$(make-exe)

include $(top_srcdir)/../automake/local.am
