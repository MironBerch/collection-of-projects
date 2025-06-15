#include <range/v3/all.hpp>
#include <AUI/View/ARadioButton.h>
#include <AUI/View/ARadioGroup.h>
#include <AUI/Model/AListModel.h>
#include "AUI/ASS/Property/BackgroundSolid.h"
#include "AUI/ASS/Property/Border.h"
#include "AUI/ASS/Property/TransformOffset.h"
#include "AUI/ASS/Selector/on_state.h"
#include "AUI/Layout/AVerticalLayout.h"
#include "AUI/Model/ATreeModel.h"
#include "AUI/View/A2FingerTransformArea.h"
#include "AUI/View/AButton.h"
#include "AUI/Layout/AHorizontalLayout.h"
#include "AUI/Platform/ACustomCaptionWindow.h"
#include "AUI/View/ACircleProgressBar.h"
#include "AUI/View/ALabel.h"
#include "AUI/Layout/AStackedLayout.h"
#include "AUI/View/ATextField.h"
#include "AUI/View/ASpacerExpanding.h"
#include "AUI/Util/UIBuildingHelpers.h"
#include "AUI/View/ASpinnerV2.h"
#include "AUI/View/AGroupBox.h"
#include "AUI/Util/ALayoutInflater.h"
#include "AUI/View/ASlider.h"
#include "AUI/Platform/APlatform.h"
#include "AUI/IO/AByteBufferInputStream.h"
#include "AUI/View/ASpinnerV2.h"
#include <AUI/i18n/AI18n.h>
#include <AUI/i18n/AI18n.h>
#include <AUI/ASS/ASS.h>
#include <AUI/View/ATextArea.h>
#include <AUI/View/ARulerView.h>
#include <AUI/View/AForEachUI.h>
#include <AUI/View/ARulerArea.h>
#include <AUI/Platform/ADesktop.h>
#include <AUI/Platform/AMessageBox.h>
#include <AUI/View/ASplitter.h>
#include <AUI/View/AScrollArea.h>
#include <AUI/View/ATabView.h>
#include <AUI/View/AGridSplitter.h>
#include <AUI/View/AText.h>
#include <AUI/View/ADrawableView.h>
#include <AUI/Traits/platform.h>

#include <memory>
#include <random>

#include "Window.h"

using namespace declarative;

void fillWindow(_<AViewContainer> t) {
    t->setLayout(std::make_unique<AStackedLayout>());
    t->addView(_new<ALabel>("Window contents"));
}

ExampleWindow::ExampleWindow() : AWindow("Examples", 800_dp, 700_dp) {
    allowDragNDrop();

    setLayout(std::make_unique<AVerticalLayout>());
    AStylesheet::global().addRules({ {
      c(".all_views_wrap") > t<AViewContainer>(),
      Padding { 16_dp },
    } });

    _<ATabView> tabView;
    _<AProgressBar> progressBar = _new<AProgressBar>();
    _<ACircleProgressBar> circleProgressBar = _new<ACircleProgressBar>();

    addView(tabView = _new<ATabView>() let {
        it->addTab(
            AScrollArea::Builder().withContents(std::conditional_t<
                                                aui::platform::current::is_mobile(), Vertical, Horizontal> {
              Vertical {
                // buttons

                GroupBox {
                  Label { "File" },
                  Vertical {
                    _new<AButton>("Create file"),
                    _new<AButton>("Save file"),
                    _new<AButton>("Open file")
                        .connect(&AView::clicked, this,
                                 [&] {
                                     mAsync << ADesktop::browseForFile(this).onSuccess([&](const APath& f) {
                                         if (f.empty()) {
                                             AMessageBox::show(this, "Result", "Cancelled");
                                         } else {
                                             AMessageBox::show(this, "Result", "File: {}"_format(f));
                                         }
                                     });
                                 }),
                    _new<AButton>("Save file as")
                        .connect(&AView::clicked, this,
                                 [&] {
                                     mAsync << ADesktop::browseForFile(this).onSuccess([&](const APath& f) {
                                         if (f.empty()) {
                                             AMessageBox::show(this, "Result", "Cancelled");
                                         } else {
                                             AMessageBox::show(this, "Result", "File: {}"_format(f));
                                         }
                                     });
                                 }),
                  },
                },
              },
              Vertical::Expanding {
                // fields

                GroupBox {
                  Label { "Fields" },
                  Vertical::Expanding {
                    Label { "Text area" },
                    AScrollArea::Builder()
                            .withContents(_new<ATextArea>(
                                "AUI Framework - Declarative UI toolkit for modern C++20\n"
                                "\n"
                                "SPDX-License-Identifier: MPL-2.0\"") with_style { FontSize { AMetric(12, AMetric::T_PX) } })
                            .build()
                        << ".input-field" let { it->setExpanding(); },
                  } }
    with_style { Expanding {} } } })
    );
        //  AText::fromString("") with_style { ATextAlign::JUSTIFY },} with_style { MinSize { 200_dp } },
        //  AText::fromString("", { WordBreak::BREAK_ALL }),} with_style { MinSize { 200_dp } },
        it->setExpanding();
    });

    addView(Horizontal {
        _new<ASpacerExpanding>(),
        _new<ALabel>("\u00a9 MironBerch, 2025") let {
            it << "#copyright";
            it->setEnabled(false);
        },
    });
}
