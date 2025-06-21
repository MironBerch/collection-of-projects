#pragma once

#include <AUI/Platform/AWindow.h>
#include "AUI/Thread/AAsyncHolder.h"


class ExampleWindow: public AWindow {
public:
	ExampleWindow();

private:
    ADeque<_<AWindow>> mWindows;
    AAsyncHolder mAsync;
};
